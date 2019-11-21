from pathlib import Path
from gensim.models.word2vec import Word2Vec
from pandas import read_csv


def make_w2v(sentence: list, model_path: str):
    '''
    CSVからモデル作成
    '''
    model = Word2Vec(sentence, size=50, window=5, min_count=3, workers=4)
    model.save(model_path)


if __name__ == "__main__":
    twitter_path = str(Path.home()) + "/py/research/twitter/"
    csv_path = twitter_path + 'a.csv'
    model_path = twitter_path + "twitter.model"
    make_w2v(
        [row.split(" ") for row in read_csv(csv_path)['wakati_text'].dropna()],
        model_path
    )
