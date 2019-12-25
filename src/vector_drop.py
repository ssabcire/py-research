from pathlib import Path
import re
from pandas import read_csv, DataFrame, Series
from pyknp import Juman


def c(csv_path):
    columns = ["label", "text", "wakati_text"]
    df = read_csv(csv_path).dropna()
    df = df.drop("vector", axis=1)
    init_df = DataFrame(columns=columns)
    for i, row in df.iterrows():
        init_df = init_df.append(
            Series([row['label'], row['text'],
                    ' '.join(_morphological_analysis(row['text']))],
                   index=columns),
            ignore_index=True)
    return init_df


def _morphological_analysis(tweet):
    '''
    tweetを形態素解析し、リストで返す
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


if __name__ == "__main__":
    cwd_data = Path().cwd() / 'data'
    valid_label_path = cwd_data / 'trend-グレタさん-valid_label.csv'
    new_csv_name = cwd_data / 'trend-グレタ-label-notVector.csv'
    c(valid_label_path).dropna().to_csv(new_csv_name, index=False)
