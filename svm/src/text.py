import re
from pyknp import Juman


def morphological_analysis(tweet: str) -> list:
    '''
    形態素解析
    '''
    jumanapp = Juman()
    result = jumanapp.analysis(_remove_unnecessary(tweet))
    return [mrph.genkei for mrph in result.mrph_list()
            if mrph.hinsi in ['名詞', '動詞', '形容詞']]


def _remove_unnecessary(tweet: str) -> str:
    return re.sub(
        r'(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)|(RT@.*?:)|([ |　])',
        '', tweet
    )
