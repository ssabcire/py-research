from pathlib import Path
from gensim.models.word2vec import Word2Vec
from numpy import zeros
from numpy.linalg import norm
from sklearn.preprocessing import StandardScaler
from pandas import read_csv


def w2v(model_path, csv_path):
    '''
    モデルを呼び出してベクトルの総和を求め、DataFrameに追加
    '''
    model = Word2Vec.load(model_path)
    df = read_csv(csv_path)
    for i, row in df.iterrows():
        # その行の総和を求める
        line_vec = _vector_from_words(row["wakati-text"].split(' '), model)
        if line_vec is not None:
            # line行に対応する列にベクトルを追加
            df.iat[i, 2] = line_vec
    return df


def _vector_from_words(words, model, normalize=False):
    '''
    単語のリストからベクトルに変換し、リストのベクトルの総和を求める
    '''
    word_vecs = []
    if len(words) == 0:
        return
    for word in words:
        word_vecs.append(model.wv[word])
    line_vec = zeros(word_vecs[0].shape, dtype=word_vecs[0].dtype)
    for word_vec in word_vecs:
        # ベクトルの総和を求める
        line_vec = line_vec + word_vec
    if normalize == True:
        return _normalize(line_vec)
    return line_vec


def _normalize(vec):
    '''
    ベクトルaのベクトルの正規化(単位ベクトルの計算)をする
    正規化で0と1の間の相対値が残る
    '''
    return vec / norm(vec)


def _all_normalize2(vec):
    '''
    標準化、これでもできないかな？
    一応、ベクトルデータ全てに対して標準化を行うので注意
    '''
    return StandardScaler().fit_transform(vec)


if __name__ == "__main__":
    twitter_path = str(Path.home()) + "/py/research/twitter/"
    csv_path = twitter_path + 'a.csv'
    model_path = twitter_path + 'twitter.model'
    df = w2v()
    df.to_csv(vector_csv_path)
