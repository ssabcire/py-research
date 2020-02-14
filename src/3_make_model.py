from pathlib import Path
from typing import List
from gensim.models.word2vec import Word2Vec
from pandas import read_csv


def make_w2v(sentence: List[List[str]], model_path: str):
    '''
    2次元リストからモデルを作成し、保存する
    '''
    model = Word2Vec(sentence, size=100, window=2, min_count=1, workers=3)
    model.save(model_path)


if __name__ == "__main__":
    cwd = Path().cwd() / 'data'
    csv_path = str(cwd / 'trend-グレタさん-label.csv')
    model_path = str(cwd / "trend-グレタさん-allTweets.model")

    make_w2v(
        [row.split(" ") for row in read_csv(csv_path)['wakati_text'].dropna()],
        str(model_path)
    )
