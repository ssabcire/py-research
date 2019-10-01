import json
import re
from glob import glob
from pyknp import Juman


def counter(text, d):
    jumanapp = Juman()
    result = jumanapp.analysis(text)
    for mrph in result.mrph_list():
        if mrph.genkei in d:
            d[mrph.genkei] = d[mrph.genkei] + 1
        else:
            d[mrph.genkei] = 1


filenames = glob('/Users/ssab/go/src/research/twitter/json/*.json')
d = dict()
for i, filename in enumerate(filenames):
    f = open(filename, 'r')
    tweet_text = json.load(f)['full_text']
    text = re.sub(
        r'(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)|(RT@.*?:)|([ |　])',
        '', tweet_text
    )
    counter(text, d)
    f.close()
print(sorted(d.items(), key=lambda x: x[1], reverse=True))
