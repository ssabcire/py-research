import re
from pyknp import Juman


def morphological_analysis(tweet: str) -> list:
    '''
    形態素解析
    '''
    text = _remove_unnecessary(tweet)
    if not text:
        return
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
    text = re.sub(
        r'(^[あ-ん]{1,2}$)|([ |　])',
        '', text
    )
    return text


if __name__ == "__main__":
    print(morphological_analysis())
