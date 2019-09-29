from pyknp import Juman


def morphological_analysis(text):
    jumanapp = Juman()
    result = jumanapp.analysis(text)
    words = set() #setでOK?
    for mrph in result.mrph_list():
        if {'名詞', '動詞', '形容詞'} in mrph.hinsi:
            words.add(mrph.genkei)
    return words
