import pytest
from src.morphological_analysis import morphological_analysis


def test_morphological_analysis():
    text = "野球をプレイする"
    expected = {"野球", "プレイ"}
    result = morphological_analysis(text)
    assert result == expected
