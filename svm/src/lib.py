import csv
import json
from glob import glob
import pandas as pd
from .text import morphological_analysis

# パスは自由に変えられるようにしたいけどコマンドライン引数にいちいち書くのめんどいしあれ
json_files = glob('a')
csv_path = 'b'
csv_name = 'c'


def make_dataframe(csv_name):
    '''
    csvファイルを読み込んで、DataFrame化
    '''
    return pd.read_csv(csv_name, encoding="utf-8")


def pre_processing():
    '''
    前処理。
    jsonファイルを読み込み、形態素解析を行い、csvに書き込む
    '''
    _write_to_csv(_load_tweet_from_file())
    _write_to_csv_using_morpho(_load_tweet_from_file())


def _load_tweet_from_file(jsonfiles: list) -> list:
    tweets = list()
    for filename in jsonfiles:
        with open(csv_name, 'w') as f:
            tweets.append(json.load(f)['full_text'])
    return tweets


header = ["id", "text"]


def _write_to_csv(tweets: list):
    with open(csv_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(
            [[i+1, tweet] for i, tweet in enumerate(tweets)]
        )


def _write_to_csv_using_morpho(tweets):
    with open(csv_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(
            [[i, ' '.join(morphological_analysis(tweet))]
             for i, tweet in enumerate(tweets)]
        )


if __name__ == '__main__':
    pre_processing()
