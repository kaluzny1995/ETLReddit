from model import EmotionResult


test_emotion_service_get_autocorrected_text_cases = [
    (None, None),
    ("", ""),
    ("I hnestly feal she'd be a beter leadr than the current lot.", "I honestly real she'd be a better leader than the current lot."),
    ("I concur. Otherwise, Carmen woud resist being picked up the second time.", "I concur. Otherwise, Carmen would resist being picked up the second time."),
    ("I see a lot of us have a worm disguised as a corgi. Our girl wiggles no matter what lol", "I see a lot of us have a worm disguised as a cgi. Our girl singles no matter what lol")
]

test_emotion_service_get_text2emotion_text_cases = [
    (None,
     EmotionResult(num_happy=0, num_angry=0, num_surprise=0, num_sad=0, num_fear=0, total_words=0)),
    ("",
     EmotionResult(num_happy=0, num_angry=0, num_surprise=0, num_sad=0, num_fear=0, total_words=0)),
    ("I honestly real she'd be a better leader than the current lot.",
     EmotionResult(num_happy=0, num_angry=0, num_surprise=1, num_sad=2, num_fear=0, total_words=6)),
    ("I concur. Otherwise, Carmen would resist being picked up the second time.",
     EmotionResult(num_happy=0, num_angry=0, num_surprise=0, num_sad=0, num_fear=1, total_words=8)),
    ("I see a lot of us have a worm disguised as a cgi. Our girl singles no matter what lol",
     EmotionResult(num_happy=0, num_angry=0, num_surprise=1, num_sad=1, num_fear=1, total_words=10))
]