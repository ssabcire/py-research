import csv
import json
import glob
from pandas import read_csv, DataFrame
from .text import morphological_analysis

# パスは自由に変えられるようにしたいけどコマンドライン引数にいちいちフルパス書くのめんどくさそう
json_files = glob.glob('a')
csv_path = 'b'
csv_name = 'c'


def make_dataframe(csv_name: str) -> DataFrame:
    '''
    csvファイルを読み込んでDataFrame化
    '''
    return read_csv(csv_name, encoding="utf-8")


def pre_processing():
    '''
    前処理
    jsonファイルを読み込み、形態素解析を行い、csvに書き込む
    '''
    _write_to_csv(_load_tweet_from_files(json_files))
    # _write_to_csv_using_morpho(_load_tweet_from_files()) # 上記とどちらかを使用


def _load_tweet_from_files(json_files: list) -> list:
    '''
    jsonファイルからツイートsを読み込む
    '''
    tweets = list()
    for filename in json_files:
        with open(csv_name, 'w') as f:
            tweets.append(json.load(f)['full_text'])
    return tweets


header = ["id", "text"]


def _write_to_csv(tweets: list):
    '''
    引数tweesをcsvに書き込む
    '''
    with open(csv_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(
            [[i+1, tweet] for i, tweet in enumerate(tweets)]
        )


def _write_to_csv_using_morpho(tweets):
    '''
    引数tweetsを形態素解析してからcsvに書き込む
    '''
    with open(csv_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(
            [[i, ' '.join(morphological_analysis(tweet))]
             for i, tweet in enumerate(tweets)]
        )


if __name__ == '__main__':
    pre_processing()
