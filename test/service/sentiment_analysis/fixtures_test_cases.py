from model import NLTKSentiment, TextblobSentiment


test_sentiment_analysis_service_get_autocorrected_text_cases = [
    (None, None),
    ("", ""),
    ("I hnestly feal she'd be a beter leadr than the current lot.", "I honestly real she'd be a better leader than the current lot."),
    ("I concur. Otherwise, Carmen woud resist being picked up the second time.", "I concur. Otherwise, Carmen would resist being picked up the second time."),
    ("I see a lot of us have a worm disguised as a corgi. Our girl wiggles no matter what lol", "I see a lot of us have a worm disguised as a cgi. Our girl singles no matter what lol")
]

test_sentiment_analysis_service_get_nltk_sentiment_cases = [
    (None, NLTKSentiment()),
    ("", NLTKSentiment()),
    ("I honestly real she'd be a better leader than the current lot.", NLTKSentiment(negative=0., neutral=0.576, positive=0.424, compound=0.7096)),
    ("I concur. Otherwise, Carmen would resist being picked up the second time.", NLTKSentiment(negative=0., neutral=1., positive=0., compound=0.)),
    ("I see a lot of us have a worm disguised as a cgi. Our girl singles no matter what lol", NLTKSentiment(negative=0.213, neutral=0.594, positive=0.193, compound=-0.1027))
]

test_sentiment_analysis_service_get_textblob_sentiment_cases = [
    (None, TextblobSentiment()),
    ("", TextblobSentiment()),
    ("I honestly real she'd be a better leader than the current lot.", TextblobSentiment(polarity=0.2333333333333333, subjectivity=0.4000000000000001)),
    ("I concur. Otherwise, Carmen would resist being picked up the second time.", TextblobSentiment(polarity=0., subjectivity=0.)),
    ("I see a lot of us have a worm disguised as a cgi. Our girl singles no matter what lol", TextblobSentiment(polarity=0.8, subjectivity=0.7))
]
