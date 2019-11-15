import re
import csv
import json
import glob
from pathlib import Path
from pyknp import Juman


def csv_processing(json_files, csv_name, header, morpho=False):
    '''
    大量のJSONファイルを読み込んでツイート部分をCSV化する
    '''
    _csv_writer(_load_files(json_files), csv_name, header, morpho)


def _load_files(files: list) -> list:
    '''
    jsonファイルからツイートsを読み込み、テキストのリストを返す
    '''
    tweets = list()
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            try:
                tweets.append(json.load(f)['full_text'])
            except json.JSONDecodeError as e:
                print("jsonDecodeError. err:", e)
                print("filename:", file)
    return tweets


def _csv_writer(
        tweets: list, csv_fname: str, header: list, morpho: bool = False):
    '''
    引数tweetsをcsvに書き込む
    morpho=Trueにすると、形態素解析を行う
    '''
    if morpho:
        with open(csv_name, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(
                [[i, tweet, ' '.join(morphological_analysis(tweet))]
                 for i, tweet in enumerate(tweets, start=1)]
            )
    else:
        with open(csv_name, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(
                [[i, tweet] for i, tweet in enumerate(tweets, start=1)]
            )


def morphological_analysis(tweet: str) -> list:
    '''
    形態素解析
    '''
    text = _remove_unnecessary(tweet)
    print('-----------------------------')
    print(tweet)
    if not text:
        return []
    return [mrph.genkei for mrph in Juman().analysis(text).mrph_list()
            if mrph.hinsi in ['名詞', '動詞', '形容詞', '接尾辞']]


def _remove_unnecessary(tweet: str) -> str:
    '''
    ツイートで不要な部分を削除
    '''
    # URL, RT@...:
    text = re.sub(
        r'(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)|(RT@.*?:)',
        '', tweet
    )
    # ツイートがひらがな1,2文字しかない場合, 空白
    # シャープ記号'#'はjumanが取り扱ってくれない。削除する必要があるかも
    text = re.sub(
        r'(^[あ-ん]{1,2}$)|([ |　])|(#)',
        '', text
    )
    return text


if __name__ == '__main__':
    twitter_path = str(Path.home()) + "/py/research/twitter/"
    json_files = glob.glob(twitter_path + "twitter-json-data/" + "*.json")
    # json_files = glob.glob(twitter_path + "twitter-json-data/2019November15-1352tweet0.json")
    csv_name = twitter_path + 'a.csv'
    header = ["id", "text", "wakati_text"]
    csv_processing(json_files, csv_name, header, morpho=True)
    # header = ["id", "text"]
    # csv_processing(json_files, csv_name, header, morpho=False)
