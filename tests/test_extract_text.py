import json
import os
from pytest import fixture
from src.extract_text import extract_text


@fixture
def create_jsonfile(tmpdir):
    data = {"full_text": "abc"}
    tmpfile = tmpdir.join('text.json')
    with tmpfile.open('w') as f:
        json.dump(
            data, f, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': ')
        )
    yield [str(tmpfile)]

    tmpfile.remove()


def test_extract_text(create_jsonfile):
    expected = ["abc"]
    texts = extract_text(create_jsonfile)
    assert texts == expected
