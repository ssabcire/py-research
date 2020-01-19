import re
import json
from pathlib import Path
from typing import Generator, List, Set
from pyknp import Juman
from pandas import DataFrame


def csv_processing(json_files: Generator[Path, None, None],
                   csv_path: Path,
                   columns: List[str]):
    '''
    ツイートであるJSONファイルを読み込んで、テキスト部分をCSV化する
    '''
    _csv_writer(_load_files(json_files), csv_path, columns)


def _load_files(json_files: Generator[Path, None, None]) -> Set[str]:
    '''
    ディレクトリからファイルすべてを読み込み、テキストのSetを返す
    '''
    tweets = set()
    for file in json_files:
        with file.open(encoding='utf-8') as f:
            try:
                tweets.add(json.load(f)['full_text'])
            except json.JSONDecodeError as e:
                print(e, "\njsofilename: ", file)
    return tweets


def _csv_writer(tweets: set, csv_path: Path, columns: List[str]):
    '''
    引数tweetsをひとつずつ形態素解析し、CSVに書き込む
    CSV1列目: ツイート, 2列目: 分かち書きされたツイート
    '''
    df = DataFrame(
        [
            (tweet, ' '.join(_morphological_analysis(tweet)))
            for tweet in tweets
        ],
        columns=columns
    )
    df.dropna().to_csv(csv_path, index=False)


def _morphological_analysis(tweet: str) -> List[str]:
    '''
    tweetを形態素解析し、リストを返す
    '''
    text = _remove_unnecessary(tweet)
    if not text:
        return []
    return [mrph.genkei for mrph in Juman().analysis(text).mrph_list()
            if mrph.hinsi in ['名詞', '動詞', '形容詞', '接尾辞']]


def _remove_unnecessary(tweet: str) -> str:
    '''
    ツイートの不要な部分を削除
    '''
    # URL, 'RT@...:', '@<ID> '
    text = re.sub(
        r'(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)|(RT@.*?:)|(@(.)+ )',
        '', tweet
    )
    # ツイートがひらがな1,2文字しかない場合, 空白
    # [", #, @] はjumanが扱えない
    return re.sub(
        r'(^[あ-ん]{1,2}$)|([ |　])|([#"@])',
        '', text
    )


if __name__ == '__main__':
    cwd = Path().cwd()
    json_files = (cwd / 'twitter' / 'trend-グレタさん').iterdir()
    csv_path = cwd / 'data' / 'trend-グレタさん.csv'
    columns = ["text", "wakati_text"]
    csv_processing(json_files, csv_path, columns)
