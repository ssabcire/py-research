from pytest import mark
from src.morphological_analysis import morphological_analysis


data = [("野球をプレイする", {"野球", "プレイ"})]
@mark.parametrize("text, expected", data)
def test_morphological_analysis(text, expected):
    result = morphological_analysis(text)
    assert result == expected
