from pyknp import Juman


def morphological_analysis(text):
    jumanapp = Juman()
    result = jumanapp.analysis(text)
    words = set()  # setだと重複消えてしまうけどOK?
    for mrph in result.mrph_list():
        if ('名詞' or '動詞' or '形容詞') in mrph.hinsi:
            words.add(mrph.genkei)
    return words
