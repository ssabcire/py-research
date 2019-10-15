from pytest import mark
from svm.src.text import _extract_text, morphological_analysis

# tweets = [("野球が好き", "野球が好き"),
#           ("ここすき https://abcde", "ここすき"),
#           ("https://abcde　ここきらい RT@wkwksn:", "ここきらい")
#           ]


# @mark.parametrize("tweet, expected", tweets)
# def test_extract_text(tweet, expected):
#     text = _extract_text(tweet)
#     assert text == expected


data = [("野球をプレイする", ["野球", "プレイ", "する"]),
        ("野球は楽しくないし、嫌い", ["野球", "楽しい", "嫌いだ"]),
        ("野球が好き", ["野球", "好きだ"])
        ]


@mark.parametrize("text, expected", data)
def test_morphological_analysis(text, expected):
    result = morphological_analysis(text)
    for word in result:
        if word not in expected:
            assert False, "expectedに含まれてない値: {0}".format(word)
    assert True
