from pytest import mark
from src.morphological_analysis import morphological_analysis


data = [("野球をプレイする", ["野球", "プレイ"]),
        ("野球は楽しくないし、嫌い", ["野球", "楽しい", "嫌いだ"]),
        ("野球が好き", ["野球", "好きだ"])
        ]


@mark.parametrize("text, expected", data)
def test_morphological_analysis(text, expected):
    '''
    形態素解析で、楽しくないが楽しいと出力されてしまうのをどうする？
    '''
    result = morphological_analysis(text)
    for word in result:
        if word not in expected:
            assert False, "expectedに含まれてない値: {0}".format(word)
    assert True
