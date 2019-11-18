import re
import json
import glob
from pathlib import Path
from pyknp import Juman
from pandas import DataFrame


def csv_processing(
        json_files: list, csv_path: str, columns: list):
    '''
    大量のJSONファイルを読み込んでツイート部分をCSV化する
    '''
    _csv_writer(_load_files(json_files), csv_path, columns)


def _load_files(json_files: list) -> set:
    '''
    jsonファイルからツイートsを読み込み、テキストのリストを返す
    '''
    tweets = set()
    for file in json_files:
        with open(file, 'r', encoding='utf-8') as f:
            try:
                tweets.add(json.load(f)['full_text'])
            except json.JSONDecodeError as e:
                print(e, "\njsofilename: ", file)
    return tweets


def _csv_writer(
        tweets: set, csv_path: str, columns: list):
    '''
    引数tweetsをcsvに書き込む
    morpho=Trueにすると、形態素解析を行う(現在は形態素解析行う場合のみを考慮している)
    '''
    df = DataFrame(
        [
            (tweet, ' '.join(_morphological_analysis(tweet)))
            for tweet in tweets
        ],
        columns=columns
    )
    df.dropna(how='any').to_csv(csv_path, index=False)


def _morphological_analysis(tweet: str) -> list:
    '''
    形態素解析
    '''
    text = _remove_unnecessary(tweet)
    if not text:
        return []
    return [mrph.genkei for mrph in Juman().analysis(text).mrph_list()
            if mrph.hinsi in ['名詞', '動詞', '形容詞', '接尾辞']]


def _remove_unnecessary(tweet: str) -> str:
    '''
    ツイートで不要な部分を削除
    '''
    # URL, 'RT@...:', '@<ID> '
    text = re.sub(
        r'(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)|(RT@.*?:)|(@(.)+ )',
        '', tweet
    )
    # ツイートがひらがな1,2文字しかない場合, 空白
    # [", #, @] はjumanが扱えない
    text = re.sub(
        r'(^[あ-ん]{1,2}$)|([ |　])|([#"@])',
        '', text
    )
    return text


if __name__ == '__main__':
    twitter_path = str(Path.home()) + "/py/research/twitter/"
    json_files = glob.glob(twitter_path + "twitter-json-data/" + "*.json")
    # json_files = glob.glob(
    #     twitter_path + "twitter-json-data/2019November15-1352tweet0.json")
    csv_path = twitter_path + 'a.csv'
    columns = ["text", "wakati_text"]
    csv_processing(json_files, csv_path, columns)
