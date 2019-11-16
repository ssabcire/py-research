from gensim.models.word2vec import Word2Vec
from numpy import zeros
from numpy.linalg import norm
from sklearn.preprocessing import StandardScaler
import pandas


def w2v(model_path, df_path):
    '''
    モデルを呼び出して、DFに書き込む
    '''
    # モデル呼び出し
    model = Word2Vec.load(model_path)
    # CSVからDataFrame作成, ツイートを呼び出す
    df = pandas.load_csv(df_path)
    # dfを1行ずつ読み込む。iterrows()やitertuples()など
    for line in df('wakati_tweet'):
        line_vec = _vector_from_words(line.split(' '), model)
        if line_vec is not None:
            # line行に対応する列にベクトルを追加
            i = df.columns.get_loc(line)
            df.iat[i, 3] = line_vec


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
    w2v()
