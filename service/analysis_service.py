import nltk
import multiprocessing
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from autocorrect import Speller
from typing import List
from tqdm import tqdm

import error
import util
from model import NLTKSentiment, TextblobSentiment, Sentiment, Reddit, Comment, Analysis
from service import IAnalysisService


class AnalysisService(IAnalysisService):
    """ Analysis service class """
    speller: Speller
    nltk_sentiment_analyzer: SentimentIntensityAnalyzer

    def __init__(self, is_multiprocessing_used: bool = False, num_processes: int = 8) -> None:
        nltk.download("vader_lexicon")

        self.speller = Speller()
        self.nltk_sentiment_analyzer = SentimentIntensityAnalyzer()
        self.is_multiprocessing_used = is_multiprocessing_used
        self.num_processes = num_processes

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

    def _process_entry(self, entry: Reddit | Comment) -> Analysis:
        """ Process single reddit or comment entry and return an analysis """
        if type(entry) not in [Reddit, Comment]:
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
            return Analysis.from_reddit(entry, autocorrected_text, sentiment)
        else:
            return Analysis.from_comment(entry, autocorrected_text, sentiment)

    def _multiprocess_entries(self, entries: List[Reddit | Comment], num: int, queue: multiprocessing.Queue) -> None:
        """ Partially processes reddit and comment entries (utilizes multiprocessing) """
        print(f"P{num + 1}: Starting processing reddit and comment entries.")

        processed_analyses = list([])
        for i, entry in enumerate(entries):
            analysis = self._process_entry(entry)
            processed_analyses.append(analysis)

            if len(processed_analyses) % 100 == 0 and len(processed_analyses) > 0:
                print(f"P{num + 1}: Processed {len(processed_analyses)} out of {len(entries)} entries.")

        print(f"P{num + 1}: Finished processing entries. Processed: {len(processed_analyses)}.")

        queue.put((processed_analyses, num))

    def run_etl(self, entries: List[Reddit | Comment]) -> List[Analysis]:
        """ Returns a list of analysis objects according to the provided reddits and comments """

        print("Processing reddits and comments:")

        analyses = list([])
        if self.is_multiprocessing_used and len(entries) > self.num_processes ** 2:
            queue = multiprocessing.Queue()
            for i, entries_chunk in enumerate(util.chunk_list_n_elements(entries, self.num_processes)):
                p = multiprocessing.Process(target=self._multiprocess_entries, args=(entries_chunk, i, queue))
                p.start()

            for i in range(self.num_processes):
                results, num = queue.get()
                analyses.extend(results)
        else:
            for entry in tqdm(entries):
                analyses.append(self._process_entry(entry))

        print("Processing finished.")

        return analyses
