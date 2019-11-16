from pathlib import Path
from gensim.models.word2vec import Word2Vec
from pandas import read_csv


def make_model(corpus: list, model_path):
    model = Word2Vec(corpus, size=100, window=5, min_count=5, workers=4)
    model.save(model_path)


if __name__ == "__main__":
    twitter_path = str(Path.home()) + "/py/research/twitter/"
    csv_path = twitter_path + 'a.csv'
    model_path = twitter_path + "twitter.model"
    make_model(read_csv(csv_path)['wakati-text'], model_path)
