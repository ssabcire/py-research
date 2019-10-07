import json
import re
from pyknp import Juman


def extract_text(filename):
    f = open(filename, 'r')
    tweet_text = json.load(f)['full_text']
    text = re.sub(
        r'(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)|(RT@.*?:)|([ |　])',
        '',
        tweet_text
    )
    f.close()
    return text


def morphological_analysis(text):
    jumanapp = Juman()
    result = jumanapp.analysis(text)
    words = set()  # ここ、SVMするときに困るから多分listのほうがいいかも？
    for mrph in result.mrph_list():
        if ('名詞' and '動詞' and '形容詞') in mrph.hinsi:
            words.add(mrph.genkei)
    return words
