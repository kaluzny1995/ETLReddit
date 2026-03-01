import nltk
import multiprocessing
import logging
import datetime as dt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from autocorrect import Speller
from typing import List
from tqdm import tqdm

import error
import util
from model import ETLParams, NLTKSentiment, TextblobSentiment, Sentiment, Reddit, Comment, SentimentAnalysis
from provider import SupabasePostgresProvider, SupabasePostgresDbSentimentAnalysisProvider, IDbRedditProvider, \
    IDbCommentProvider, IDbSentimentAnalysisProvider, SupabasePostgresDbRedditProvider, \
    SupabasePostgresDbCommentProvider
from service import ISentimentAnalysisService


class SentimentAnalysisService(ISentimentAnalysisService):
    """ SentimentAnalysis service class """
    logger: logging.Logger
    reddit_provider: IDbRedditProvider
    comment_provider: IDbCommentProvider
    sentiment_analysis_provider: IDbSentimentAnalysisProvider

    speller: Speller
    nltk_sentiment_analyzer: SentimentIntensityAnalyzer

    def __init__(self, logger: logging.Logger | None = None,
                 reddit_provider: IDbRedditProvider | None = None,
                 comment_provider: IDbCommentProvider | None = None,
                 sentiment_analysis_provider: IDbSentimentAnalysisProvider | None = None) -> None:
        nltk.download("vader_lexicon")

        self.logger = logger or util.setup_logger(name="sentiment_analysis_service",
                                                  log_file=f"logs/other/sentiment_analysis_service.log")

        supabase_postgres_provider = SupabasePostgresProvider(logger=self.logger)
        self.reddit_provider = reddit_provider or SupabasePostgresDbRedditProvider(supabase_postgres_provider)
        self.comment_provider = comment_provider or SupabasePostgresDbCommentProvider(supabase_postgres_provider)
        self.sentiment_analysis_provider = sentiment_analysis_provider or SupabasePostgresDbSentimentAnalysisProvider(supabase_postgres_provider)
        self.speller = Speller()
        self.nltk_sentiment_analyzer = SentimentIntensityAnalyzer()


    def get_autocorrected_text(self, text: str | None) -> str | None:
        """ Returns the autocorrected text """
        return None if text is None else self.speller(text)

    def get_nltk_sentiment(self, text: str | None) -> NLTKSentiment:
        """ Returns the NLTK sentiment """
        if text is None:
            return NLTKSentiment()
        else:
            sentiments = self.nltk_sentiment_analyzer.polarity_scores(text)
            return NLTKSentiment(negative=sentiments['neg'], neutral=sentiments['neu'],
                                 positive=sentiments['pos'], compound=sentiments['compound'])

    def get_textblob_sentiment(self, text: str | None) -> TextblobSentiment:
        """ Returns the textblob sentiment """
        if text is None:
            return TextblobSentiment()
        else:
            sentiments = TextBlob(text).sentiment
            return TextblobSentiment(polarity=sentiments.polarity, subjectivity=sentiments.subjectivity)

    def _get_sentiment_analyses(self, entries: List[Reddit | Comment], params: ETLParams) -> List[SentimentAnalysis]:
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

    def _process_entry(self, entry: Reddit | Comment) -> SentimentAnalysis:
        """ Processes single reddit or comment entry and return sentiment analysis """
        if type(entry) not in [Reddit, Comment]:
            self.logger.error(f"The provided entity for ETL has improper type: {type(entry)}.")
            raise error.WrongEntityError(f"The provided entity for ETL has improper type: {type(entry)}.")

        if isinstance(entry, Reddit):
            dirty_text = entry.title if entry.body is None else f"{entry.title} | {entry.body}"
        else:
            dirty_text = None if entry.body is None else entry.body
        autocorrected_text = self.get_autocorrected_text(dirty_text)
        nltk_sentiment = self.get_nltk_sentiment(autocorrected_text)
        textblob_sentiment = self.get_textblob_sentiment(autocorrected_text)
        sentiment = Sentiment.from_ntlk_and_textblob(nltk_sentiment, textblob_sentiment)

        if isinstance(entry, Reddit):
            return SentimentAnalysis.from_reddit(entry, autocorrected_text, sentiment)
        else:
            return SentimentAnalysis.from_comment(entry, autocorrected_text, sentiment)

    def _multiprocess_entries(self, entries: List[Reddit | Comment], num: int, queue: multiprocessing.Queue) -> None:
        """ Partially processes reddit and comment entries (utilizes multiprocessing) """
        print(f"P{num + 1}: Starting processing reddit and comment entries.")
        self.logger.info(f"P{num + 1}: Starting processing reddit and comment entries.")

        processed_sentiment_analyses = list([])
        for i, entry in enumerate(entries):
            sentiment_analysis = self._process_entry(entry)
            processed_sentiment_analyses.append(sentiment_analysis)

            if len(processed_sentiment_analyses) % 100 == 0 and len(processed_sentiment_analyses) > 0:
                print(f"P{num + 1}: Processed {len(processed_sentiment_analyses)} out of {len(entries)} entries.")
                self.logger.info(f"P{num + 1}: Processed {len(processed_sentiment_analyses)} out of {len(entries)} entries.")

        print(f"P{num + 1}: Finished processing entries. Processed: {len(processed_sentiment_analyses)}.")
        self.logger.info(f"P{num + 1}: Finished processing entries. Processed: {len(processed_sentiment_analyses)}.")

        queue.put((processed_sentiment_analyses, num))

    def run_etl(self, **etl_params_dict) -> None:
        """ Runs ETL process loading expected reddits and comments, processing and persisting expected sentiment analyses """
        etl_params = ETLParams(**etl_params_dict)

        print("Starting sentiment analysis ETL process.")
        self.logger.info("Starting sentiment analysis ETL process.")

        # load source file dates
        source_file_dates = sorted(self.reddit_provider.get_file_dates(phrase=etl_params.phrase))
        print("Source file dates:\n", source_file_dates)
        self.logger.info(f"Source file dates: {source_file_dates}")

        # load target files dates
        target_file_dates = sorted(self.sentiment_analysis_provider.get_file_dates(phrase=etl_params.phrase))
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

        sentiment_analyses = self._get_sentiment_analyses(entries, etl_params)

        print(f"Sentiment analyses processed: {len(sentiment_analyses)}.\n")
        self.logger.info(f"Sentiment analyses processed: {len(sentiment_analyses)}.")

        # file date gaps detection and filling in with blank records
        if etl_params.is_filled_missing_dates:
            print("Searching for missing file dates.")
            self.logger.info("Searching for missing file dates.")

            file_dates = self.sentiment_analysis_provider.get_file_dates(etl_params.phrase)
            file_dates.extend(list(map(lambda sa: sa.file_date, sentiment_analyses)))
            file_dates = sorted(set(file_dates))

            checked_date_periods = util.date_range(
                start_date=dt.datetime.strptime(etl_params.start_date, "%Y-%m-%d"),
                end_date=dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - dt.timedelta(seconds=1) \
                    if etl_params.is_until_previous_day else dt.datetime.now(),
                interval=etl_params.date_interval
            )
            is_missing_found = False
            for start_date, end_date in checked_date_periods:
                if start_date.isoformat() not in file_dates:
                    print(f"No data for file date '{start_date}'. Inserting blank record.")
                    self.logger.info(f"No data for file date '{start_date}'. Inserting blank record.")
                    is_missing_found = True
                    sentiment_analyses.append(SentimentAnalysis.blank(etl_params.phrase, start_date.isoformat()))
            if not is_missing_found and len(missing_file_dates) == 0:
                print("No new data available. Finishing.")
                self.logger.info(f"No new data available. Finishing.")
                raise error.NoNewDataError("No new data available for ETL.")

        # insert sentiment analyses
        self.sentiment_analysis_provider.insert_sentiment_analyses(sentiment_analyses, batch_size=etl_params.batch_size)

        print("Sentiment analysis ETL process finished.")
        self.logger.info("Sentiment analysis ETL process finished.")
