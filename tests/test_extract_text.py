import json
import os
from pytest import fixture
from src.extract_text import extract_text


def test_extract_text(create_jsonfile):
    expected = "野球が好き"
    text = extract_text(create_jsonfile)
    assert text == expected
