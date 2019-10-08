import json
import re
from pyknp import Juman


def create_tweets_loading_file(jsonfiles: list) -> list:
    tweets = list()
    for filename in jsonfiles:
        f = open(filename, 'r')
        tweet = json.load(f)['full_text']
        tweets.append(tweet)
        f.close()
    return tweets


def morphological_analysis(tweet: str) -> list:
    '''
    形態素解析
    '''
    jumanapp = Juman()
    result = jumanapp.analysis(_extract_text(tweet))
    words = list()
    for mrph in result.mrph_list():
        if ('名詞' and '動詞' and '形容詞') in mrph.hinsi:
            words.append(mrph.genkei)
    return words


def _extract_text(tweet: str) -> str:
    return re.sub(
        r'(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)|(RT@.*?:)|([ |　])',  # 修正必要
        '',
        tweet
    )
