from gensim.models.word2vec import Word2Vec


def make_model():
    # csvなどから2次元配列などを作成。DataFrameなどでもよさそう
    # sentences = df['text'] てきな
    # モデルを作成
    Word2Vec(
        sentences, min_count=1
    ).save("w2v-twitter.model")


if __name__ == "__main__":
    make_model()
