import csv
import json
import glob
from .text import morphological_analysis


def csv_processing(json_files, csv_name, header, molpho=False):
    '''
    CSVへの処理
    jsonファイルを読み込み、形態素解析を行い、csvに書き込む
    '''
    _write_to_csv(
        _load_tweet_from_files(json_files), header, csv_name, molpho=False
    )


def _load_tweet_from_files(json_files: list) -> list:
    '''
    jsonファイルからツイートsを読み込む
    '''
    tweets = list()
    for filename in json_files:
        with open(csv_name, 'w') as f:
            tweets.append(json.load(f)['full_text'])
    return tweets


def _write_to_csv(
        tweets: list, csv_name: str, header: list, morpho: bool = False):
    '''
    引数tweesをcsvに書き込む
    morpho=Trueにすると、形態素解析を行う
    '''
    if morpho:
        with open(csv_name, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(
                [[i, ' '.join(morphological_analysis(tweet))]
                 for i, tweet in enumerate(tweets, start=1)]
            )
    else:
        with open(csv_name, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(
                [[i, tweet] for i, tweet in enumerate(tweets, start=1)]
            )


if __name__ == '__main__':
    json_files = glob.glob('a')
    csv_path = 'b'
    csv_name = 'c'
    header = ["id", "text"]
    csv_processing(json_files, csv_name, header, molpho=True)
