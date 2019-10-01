import json
from pytest import fixture

@fixture
def create_jsonfile(tmpdir):
    data = {"full_text": "abc"}
    tmpfile = tmpdir.join('text.json')
    with tmpfile.open('w') as f:
        json.dump(
            data, f, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': ')
        )
    yield str(tmpfile)
    tmpfile.remove()
