from pathlib import Path
from gensim.models.word2vec import Word2Vec
from numpy import zeros
from numpy.linalg import norm
from sklearn.preprocessing import StandardScaler
from pandas import read_csv


def vector_sum(model_path, csv_path):
    '''
    DataFrameのwakati_textを1行ずつ単語ベクトルの総和を求める
    総和をDataFrameに追加
    '''
    model = Word2Vec.load(model_path)
    df = read_csv(csv_path)
    # .dropnaしたあとにi, 2などをすると、要素番号がずれてしまうので一致しない可能性がある。その対処
    wakati_texts = [row.split(" ") for row in df(csv_path)['wakati_text']
                    .dropna(how='any').values.tolist()]
    for i, row in wakati_texts:
        # 改善必要...?
        df.iat[i, 2] = _vector_from_words(row, model)
    return df


def _vector_from_words(row: list, model, normalize=False):
    # 改善必要
    '''
    row: 1ツイートを形態素解析した単語のリスト
    model: Word2Vecモデル
    単語のリストからベクトルに変換し、リストのベクトルの総和を求める
    '''
    word_vecs = []
    for word in row:
        word_vecs.append(model.wv[word])
    line_vec = zeros(word_vecs[0].shape, dtype=word_vecs[0].dtype)
    for word_vec in word_vecs:
        # ベクトルの総和を求める
        line_vec = line_vec + word_vec
    if not normalize:
        return line_vec
    return _normalize(line_vec)


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
    vector_csv_path = twitter_path + 'b.csv'
    model_path = twitter_path + 'twitter.model'
    df = w2v()
    df.to_csv(vector_csv_path)
