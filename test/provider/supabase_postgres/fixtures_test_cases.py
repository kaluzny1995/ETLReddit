import datetime as dt

from model import Author, Reddit, Comment, SentimentAnalysis

authors = [
    Author(name="MooseWhisperer09",
           background_color=None, css_class=None, richtext=None,
           template_id=None, text=None, text_color=None, type="text", fullname="t2_cqmfh",
           is_blocked=False, is_patreon_flair=False, is_premium=False,
           datetime_created=dt.datetime(2025, 9, 2, 20, 8, 51),
           datetime_created_utc=dt.datetime(2025, 9, 2, 20, 8, 51),
           permalink="/r/nextfuckinglevel/comments/1n6muyq/an_enormous_moose_approaches_the_camera_and_get/nc1yqtj/"
    ),
    Author(name="ch0c0l2te",
           background_color=None, css_class="forsure", richtext="[{\"e\": \"text\", \"t\": \"BWOAHHHHHHH \"}]",
           template_id=None, text="BWOAHHHHHHH ", text_color="dark", type="richtext", fullname="t2_h51w2",
           is_blocked=False, is_patreon_flair=False, is_premium=True,
           datetime_created=dt.datetime(2026, 1, 17, 14, 52, 1),
           datetime_created_utc=dt.datetime(2026, 1, 17, 14, 52, 1),
           permalink="/r/formuladank/comments/1qerdow/its_about_time/o03rw1q/"
    ),
    Author(name="OmdiAnomenkinshin",
           background_color=None, css_class=None, richtext=None,
           template_id=None, text=None, text_color=None, type="text", fullname="t2_7k1sc",
           is_blocked=False, is_patreon_flair=False, is_premium=False,
           datetime_created=dt.datetime(2021, 3, 7, 20, 45, 29),
           datetime_created_utc=dt.datetime(2021, 3, 7, 20, 45, 29),
           permalink="/r/imaginarymaps/comments/lzy1e3/turning_countries_into_holy_roman_empires_bhutan/"
    ),
    Author(name="aarretuli",
           background_color="cyan", css_class="flair-uusimaa", richtext="[{\"e\": \"text\", \"t\": \"\u2728\u2728\"}]",
           template_id="8d550740-8fed-11e3-b899-22000ab83216", text="\u2728\u2728", text_color="dark", type="richtext", fullname="t2_1738uera",
           is_blocked=False, is_patreon_flair=False, is_premium=False,
           datetime_created=dt.datetime(2026, 1, 24, 10, 24, 17),
           datetime_created_utc=dt.datetime(2026, 1, 24, 10, 24, 17),
           permalink="/r/Suomi/comments/1qkyue6/lasten_turvaruoan_tarve_on_kasvanut_vanhemmat/o1ekf3z/"
    )
]

reddits = [
    Reddit(reddit_id="jgz2uz", name="t3_jgz2uz",
           permalink="/r/aww/comments/jgz2uz/we_live_in_a_basement_suite_so_i_built_a_loft_for/",
           phrase="corgi", author="CocaKoller",
           title="We live in a basement suite. So I built a loft for our corgi Wolfgang.",
           body=None,
           datetime_created=dt.datetime(2020, 10, 24, 0, 14, 42),
           datetime_created_utc=dt.datetime(2020, 10, 24, 0, 14, 42),
           likes=None, ups=115320, downs=0, score=115320, upvote_ratio=0.94, gilded_number=4, number_of_comments=820,
           start_file_date="2026-01-01", end_file_date="2027-01-01"
    ),
    Reddit(reddit_id="135yzs1", name="t3_135yzs1",
           permalink="/r/BrandNewSentence/comments/135yzs1/corgisized_meteor_as_heavy_as_4_baby_elephants/",
           phrase="corgi", author="HELL-OAT",
           title="Corgi-sized meteor as heavy as 4 baby elephants",
           body="That's amazing!",
           datetime_created=dt.datetime(2023, 5, 2, 20, 18, 4),
           datetime_created_utc=dt.datetime(2023, 5, 2, 20, 18, 4),
           likes=37, ups=37097, downs=0, score=37097, upvote_ratio=0.96, gilded_number=0, number_of_comments=643,
           start_file_date="2022-01-01", end_file_date="2023-01-01"
    ),
    Reddit(reddit_id="ip48w1m", name="t1_ip48w1m",
           permalink="/r/CasualUK/comments/xijejh/queen_elizabeth_ii_corgis_waiting_outside_the/",
           phrase="corgi", author="Feisty-Donkey",
           title="Queen Elizabeth II corgis waiting outside the procession for her coffin to arrive.",
           body="Candy, the dorgi, died earlier this summer. Media reported it sometime in the last week",
           datetime_created=dt.datetime(2022, 9, 19, 20, 18, 4),
           datetime_created_utc=dt.datetime(2022, 9, 19, 20, 18, 4),
           likes=0, ups=124, downs=0, score=124, upvote_ratio=1., gilded_number=2, number_of_comments=16,
           start_file_date="2022-01-01", end_file_date="2023-01-01"
    ),
    Reddit(reddit_id="1e2b04h", name="t3_1e2b04h",
           permalink="/r/corgi/comments/1e2b04h/whos_corgi_has_a_human_name/",
           phrase="corgi", author="infantkicker_v2",
           title="Who's corgi has a \"human\" name?",
           body="This is Tony. When we got him we called him bologna which evolved to Tony bologna and eventually just Tony. Unless he's being bad, then he's ANTHONY!.",
           datetime_created=dt.datetime(2024, 7, 13, 13, 55, 55),
           datetime_created_utc=dt.datetime(2024, 7, 13, 13, 55, 55),
           likes=0, ups=2588, downs=0, score=2588, upvote_ratio=0.95, gilded_number=0, number_of_comments=787,
           start_file_date="2024-01-01", end_file_date="2025-01-01"
    )
]

comments = [
    Comment(comment_id="g9tw6ow", reddit_id="g9tw6ow", parent_comment_id=None, name="t1_g9tw6ow",
            permalink="/r/aww/comments/jgz2uz/we_live_in_a_basement_suite_so_i_built_a_loft_for/g9tw6ow/",
            phrase="corgi", author=None,
            body="I like Wolfgang.",
            datetime_created=dt.datetime(2020, 10, 24, 3, 6, 39),
            datetime_created_utc=dt.datetime(2020, 10, 24, 3, 6, 39),
            depth_level=0, controversiality=False,
            likes=0, ups=1013, downs=0, score=1013, upvote_ratio=1., gilded_number=0, number_of_replies=7,
            start_file_date="2022-01-01", end_file_date="2023-01-01"
    ),
    Comment(comment_id="g9v8jbi", reddit_id="g9tw6ow", parent_comment_id="g9u5mh6", name="t1_g9v8jbi",
            permalink="/r/aww/comments/jgz2uz/we_live_in_a_basement_suite_so_i_built_a_loft_for/g9v8jbi/",
            phrase="corgi", author="rognabologna",
            body="Please tell me he's named Wolfgang Puck, after the chef, but you call him Wolfgang Pup",
            datetime_created=dt.datetime(2020, 10, 24, 8, 50, 1),
            datetime_created_utc=dt.datetime(2020, 10, 24, 8, 50, 1),
            depth_level=2, controversiality=True,
            likes=18, ups=72, downs=0, score=72, upvote_ratio=1., gilded_number=3, number_of_replies=0,
            start_file_date="2026-01-01", end_file_date="2027-01-01"
    ),
    Comment(comment_id="lczs45r", reddit_id="1e2b04h", parent_comment_id=None, name="t1_lczs45r",
            permalink="/r/corgi/comments/1e2b04h/whos_corgi_has_a_human_name/lczs45r/",
            phrase="corgi", author="SparkleWildfire",
            body="This is Ella. She is named after my late Grandma. She is cute, stubborn, very funny, and we spend a lot of time discussing her toilet habits. Basically it is the perfect name for her.\n\nAlso often manages to look awkward in photos. See Exhibit A.\n\nhttps://preview.redd.it/pm5e1aenpacd1.jpeg?width=3072&amp;format=pjpg&amp;auto=webp&amp;s=39dbe0a0eb2aba067dddbdea2f6b7d4028ce167f",
            datetime_created=dt.datetime(2024, 7, 13, 14, 23, 54),
            datetime_created_utc=dt.datetime(2024, 7, 13, 14, 23, 54),
            depth_level=0, controversiality=False,
            likes=0, ups=373, downs=0, score=373, upvote_ratio=1., gilded_number=0, number_of_replies=41,
            start_file_date="2024-01-01", end_file_date="2025-01-01"
    ),
    Comment(comment_id="ip48e6j", reddit_id="1e2b04h", parent_comment_id="ip44v7j", name="t1_ip48e6j",
            permalink="/r/CasualUK/comments/xijejh/queen_elizabeth_ii_corgis_waiting_outside_the/ip48e6j/",
            phrase="corgi", author=None,
            body="I read in one of the sixty million articles about the Queen that she had given up keeping corgis, because she didn't want to leave them bereft when she died. But Prince Andrew decided to give her two for her birthday last year. That's why he's inheriting them. There's also still a dorgi kicking around apparently.",
            datetime_created=dt.datetime(2022, 9, 19, 21, 35, 52),
            datetime_created_utc=dt.datetime(2022, 9, 19, 21, 35, 52),
            depth_level=3, controversiality=False,
            likes=0, ups=144, downs=0, score=144, upvote_ratio=1., gilded_number=0, number_of_replies=16,
            start_file_date="2022-01-01", end_file_date="2024-01-01"
    )
]

sentiment_analyses = [
    SentimentAnalysis(reddit_id="jgz2uz", comment_id="N/A", phrase="corgi", author="CocaKoller",
                      text="We live in a basement suite. So I built a loft for our cgi Wolfgang.",
                      datetime_created=dt.datetime(2020, 10, 24, 0, 14, 42),
                      score=115320, upvote_ratio=0.94, gilded_number=4, number_of_comments=820,
                      controversiality=False,
                      s_neg=0., s_neu=1., s_pos=0., s_com=0., s_pol=0.13636363636363635, s_sub=0.5,
                      file_date="2026-01-01"
    ),
    SentimentAnalysis(reddit_id="135yzs1", comment_id="N/A", phrase="corgi", author="HELL-OAT",
                      text="Corgi-sized meteor as heavy as 4 baby elephants",
                      datetime_created=dt.datetime(2023, 5, 2, 20, 18, 4),
                      score=37097, upvote_ratio=0.96, gilded_number=0, number_of_comments=643,
                      controversiality=False,
                      s_neg=0., s_neu=1., s_pos=0., s_com=0., s_pol=-0.2, s_sub=0.5,
                      file_date="2022-01-01"
    ),
    SentimentAnalysis(reddit_id="N/A", comment_id="fddgp16", phrase="aussie", author="num1AusDoto",
                      text="Man people really be listening to that man but not a scientist fuck me dead can the fires just take me",
                      datetime_created=dt.datetime(2020, 1, 6, 12, 51, 33),
                      score=89, upvote_ratio=1., gilded_number=0, number_of_comments=0,
                      controversiality=False,
                      s_neg=0.215, s_neu=0.649, s_pos=0.136, s_com=-0.4897, s_pol=-0.1333, s_sub=0.4,
                      file_date="2020-01-01"
    ),
    SentimentAnalysis(reddit_id="N/A", comment_id="fddgv1o", phrase="aussie", author="LeonardDeVir",
                      text="She will find better people for her life after her deed.",
                      datetime_created=dt.datetime(2020, 1, 6, 12, 55, 3),
                      score=268, upvote_ratio=1., gilded_number=0, number_of_comments=0,
                      controversiality=False,
                      s_neg=0., s_neu=0.775, s_pos=0.225, s_com=-0.4404, s_pol=0.5, s_sub=0.5,
                      file_date="2020-01-01"
    )
]
