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
    return [mrph.genkei for mrph in result.mrph_list()
            if mrph.hinsi in ['名詞', '動詞', '形容詞']]


# def dependency_analysis(tweet: str) -> list:
#     '''(未完成)
#     基本句単位で係り受け解析
#     return: 格解析されたツイートのリスト [(格関係体言, 格関係用言), ...]
#     '''
#     jumanapp = Juman()
#     result = jumanapp.analysis(_extract_text(tweet))
#     temp_dependencies = list()
#     for tag in result.tag_list:
#         if '<格関係' in tag.fstring:
#             dependency_words += re.findall(r'<格関係[0-9]:.*?>')
#     dependency_words = list()
#     for substantives, inflections in temp_dependencies:
#         re.sub(r'', '', inflections)
#         dependency_words.append(
#             (substantives+'ガなどの格助詞', '抽出したinflections')
#         )
#     return dependency_words


def _extract_text(tweet: str) -> str:
    return re.sub(
        r'(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)|(RT@.*?:)|([ |　])',
        '', tweet
    )
