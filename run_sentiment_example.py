from model import SentimentResult
from service import SentimentService


def main():
    input_text = "I hnestly feal she'd be a beter leadr than the current lot."
    print("Input text: ", input_text)
    sentiment_service = SentimentService()

    clean_text = sentiment_service.get_autocorrected_text(input_text)
    print("Cleaned text: ", clean_text)

    nltk_sentiment = sentiment_service.get_nltk_sentiment(clean_text)
    print("NLTK sentiment: ", nltk_sentiment)

    textblob_sentiment = sentiment_service.get_textblob_sentiment(clean_text)
    print("Textblob sentiment: ", textblob_sentiment)

    sentiment_result = SentimentResult.from_ntlk_and_textblob(nltk_sentiment, textblob_sentiment)
    print("Sentiment result: ", sentiment_result)


if __name__ == "__main__":
    main()
