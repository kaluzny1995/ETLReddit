import nltk
import multiprocessing
import logging
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from autocorrect import Speller
from typing import List
from tqdm import tqdm

import error
import util
from model import NLTKSentiment, TextblobSentiment, Sentiment, Reddit, Comment, SentimentAnalysis
from service import ISentimentAnalysisService


class SentimentAnalysisService(ISentimentAnalysisService):
    """ SentimentAnalysis service class """
    speller: Speller
    nltk_sentiment_analyzer: SentimentIntensityAnalyzer
    logger: logging.Logger

    def __init__(self, is_multiprocessing_used: bool = False, num_processes: int = 8,
                 logger: logging.Logger | None = None) -> None:
        nltk.download("vader_lexicon")

        self.speller = Speller()
        self.nltk_sentiment_analyzer = SentimentIntensityAnalyzer()
        self.is_multiprocessing_used = is_multiprocessing_used
        self.num_processes = num_processes
        self.logger = logger or util.setup_logger(name="sentiment_analysis_service",
                                                  log_file=f"logs/other/sentiment_analysis_service.log")

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

    def _process_entry(self, entry: Reddit | Comment) -> SentimentAnalysis:
        """ Process single reddit or comment entry and return sentiment analysis """
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

    def run_etl(self, entries: List[Reddit | Comment]) -> List[SentimentAnalysis]:
        """ Returns a list of sentiment analysis objects according to the provided reddits and comments """

        print("Processing reddits and comments:")
        self.logger.info("Processing reddits and comments.")

        sentiment_analyses = list([])
        if self.is_multiprocessing_used and len(entries) > self.num_processes ** 2:
            queue = multiprocessing.Queue()
            for i, entries_chunk in enumerate(util.chunk_list_n_elements(entries, self.num_processes)):
                p = multiprocessing.Process(target=self._multiprocess_entries, args=(entries_chunk, i, queue))
                p.start()

            for i in range(self.num_processes):
                results, num = queue.get()
                sentiment_analyses.extend(results)
        else:
            for entry in tqdm(entries):
                sentiment_analyses.append(self._process_entry(entry))

        print("Processing finished.")
        self.logger.info("Processing finished.")

        return sentiment_analyses
