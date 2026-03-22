import multiprocessing
import logging
from typing import List
from tqdm import tqdm
from autocorrect import Speller

import error
import util
import text2emotion
from model import ETLParams, EmotionResult, Reddit, Comment, Emotion
from provider import IDbRedditProvider, IDbCommentProvider, IDbEmotionProvider, \
    SupabasePostgresProvider, SupabasePostgresDbRedditProvider, \
    SupabasePostgresDbCommentProvider, SupabasePostgresDbEmotionProvider
from service import IEmotionService


class EmotionService(IEmotionService):
    """ Emotion service class """

    logger: logging.Logger
    reddit_provider: IDbRedditProvider
    comment_provider: IDbCommentProvider
    emotion_provider: IDbEmotionProvider

    speller: Speller

    def __init__(self, logger: logging.Logger | None = None,
                 reddit_provider: IDbRedditProvider | None = None,
                 comment_provider: IDbCommentProvider | None = None,
                 emotion_provider: IDbEmotionProvider | None = None) -> None:
        self.logger = logger or util.setup_logger(name="emotion_service",
                                                  log_file=f"logs/other/emotion_service.log")

        supabase_postgres_provider = SupabasePostgresProvider(logger=self.logger)
        self.reddit_provider = reddit_provider or SupabasePostgresDbRedditProvider(supabase_postgres_provider)
        self.comment_provider = comment_provider or SupabasePostgresDbCommentProvider(supabase_postgres_provider)
        self.emotion_provider = emotion_provider or SupabasePostgresDbEmotionProvider(supabase_postgres_provider)

        self.speller = Speller()

    def get_autocorrected_text(self, text: str | None) -> str | None:
        """ Returns the autocorrected text """
        return None if text is None else self.speller(text)

    def get_text2emotion(self, text: str | None) -> EmotionResult:
        """ Returns the emotion result from given text """
        text2emotion_result, total_words = text2emotion.get_emotion(text)
        return EmotionResult(
            num_happy=text2emotion_result['Happy'],
            num_angry=text2emotion_result['Angry'],
            num_surprise=text2emotion_result['Surprise'],
            num_sad=text2emotion_result['Sad'],
            num_fear=text2emotion_result['Fear'],
            total_words=total_words
        )

    def get_emotions(self, entries: List[Reddit | Comment], params: ETLParams) -> List[Emotion]:
        """ Returns the processed emotions from given entries """
        results = list([])
        if params.is_multiprocessing_used and len(entries) > params.num_processes ** 2:
            queue = multiprocessing.Queue()
            for i, entries_chunk in enumerate(util.chunk_list_n_elements(entries, params.num_processes)):
                p = multiprocessing.Process(target=self._multiprocess_entries, args=(entries_chunk, i, queue))
                p.start()

            for i in range(params.num_processes):
                results_chunk, num = queue.get()
                results.extend(results_chunk)
        else:
            for entry in tqdm(entries):
                results.append(self._process_entry(entry))
        return results


    def _process_entry(self, entry: Reddit | Comment) -> Emotion:
        """ Processes single reddit or comment entry and returns emotion """
        if type(entry) not in [Reddit, Comment]:
            self.logger.error(f"The provided entity for ETL has improper type: {type(entry)}.")
            raise error.WrongEntityError(f"The provided entity for ETL has improper type: {type(entry)}.")

        if isinstance(entry, Reddit):
            dirty_text = entry.title if entry.body is None else f"{entry.title} {entry.body}"
        else:
            dirty_text = None if entry.body is None else entry.body
        autocorrected_text = self.get_autocorrected_text(dirty_text)
        emotion_result = self.get_text2emotion(autocorrected_text)

        if isinstance(entry, Reddit):
            return Emotion.from_reddit(entry, emotion_result)
        else:
            return Emotion.from_comment(entry, emotion_result)

    def _multiprocess_entries(self, entries: List[Reddit | Comment], num: int, queue: multiprocessing.Queue) -> None:
        """ Partially processes reddit and comment entries (utilizes multiprocessing) """
        print(f"P{num + 1}: Starting processing reddit and comment entries.")
        self.logger.info(f"P{num + 1}: Starting processing reddit and comment entries.")

        processed_emotions = list([])
        for i, entry in enumerate(entries):
            emotion = self._process_entry(entry)
            processed_emotions.append(emotion)

            if len(processed_emotions) % 100 == 0 and len(processed_emotions) > 0:
                print(f"P{num + 1}: Processed {len(processed_emotions)} out of {len(entries)} entries.")
                self.logger.info(f"P{num + 1}: Processed {len(processed_emotions)} out of {len(entries)} entries.")

        print(f"P{num + 1}: Finished processing entries. Processed: {len(processed_emotions)}.")
        self.logger.info(f"P{num + 1}: Finished processing entries. Processed: {len(processed_emotions)}.")

        queue.put((processed_emotions, num))

    def run_etl(self, **etl_params_dict) -> None:
        """ Runs ETL process loading expected reddits and comments, processing and persisting expected emotions """
        etl_params = ETLParams(**etl_params_dict)

        print("Starting emotion ETL process.")
        self.logger.info("Starting emotion ETL process.")

        # load source file dates
        source_file_dates = sorted(self.reddit_provider.get_file_dates(phrase=etl_params.phrase))
        print("Source file dates:\n", source_file_dates)
        self.logger.info(f"Source file dates: {source_file_dates}")

        # load target files dates
        target_file_dates = sorted(self.emotion_provider.get_file_dates(phrase=etl_params.phrase))
        print("Target file dates:\n", target_file_dates)
        self.logger.info(f"Target file dates: {target_file_dates}")
        recent_target_file_date = None if len(target_file_dates) == 0 else target_file_dates[-1]
        print("Recent target file date:", recent_target_file_date)
        self.logger.info(f"Recent target file date: {recent_target_file_date}")
        print()

        # determine the missing file dates to load the data for
        missing_file_dates = source_file_dates if recent_target_file_date is None \
            else list(filter(lambda fd: fd > recent_target_file_date, source_file_dates))
        if not etl_params.is_filled_missing_dates and len(missing_file_dates) == 0:
            print("No new data available. Finishing.")
            self.logger.info(f"No new data available. Finishing.")
            raise error.NoNewDataError("No new data available for ETL.")
        print(f"\nLoading data for the following dates:\n{missing_file_dates}\n")
        self.logger.info(f"Loading data for the following dates: {missing_file_dates}")

        # get reddit and comment entries
        reddits = self.reddit_provider.get_reddits(phrase=etl_params.phrase, file_dates=missing_file_dates)
        comments = self.comment_provider.get_comments(phrase=etl_params.phrase, file_dates=missing_file_dates)
        entries = reddits + comments

        print("Reddit and comment entries loaded:", len(entries))
        self.logger.info(f"Reddit and comment entries loaded: {len(entries)}")

        # process reddit and comment entries
        print("Processing reddits and comments:")
        self.logger.info("Processing reddits and comments.")

        emotions = self.get_emotions(entries, etl_params)

        print(f"Popularities processed: {len(emotions)}.\n")
        self.logger.info(f"Popularities processed: {len(emotions)}.")

        # file date gaps detection and filling in with blank records
        if etl_params.is_filled_missing_dates:
            print("Warning. Filling in for missing dates not supported for emotion ETL process.")
            self.logger.warning("Warning. Filling in for missing dates not supported for emotion ETL process.")

        # insert emotions
        self.emotion_provider.insert_emotions(emotions, batch_size=etl_params.batch_size)

        print("Emotion ETL process finished.")
        self.logger.info("Emotion ETL process finished.")
