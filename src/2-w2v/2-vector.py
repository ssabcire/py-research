from pathlib import Path
from gensim.models.word2vec import Word2Vec
from typing import List
from numpy import zeros, ndarray
from numpy.linalg import norm
from pandas import read_csv, DataFrame


def df_vector(csv_path: Path, model_path: Path) -> DataFrame:
    '''
    DataFrameのwakati_textを1行ずつ単語ベクトルの総和を求める
    総和をDataFrameに追加
    '''
    model = Word2Vec.load(model_path)
    df = read_csv(csv_path)['wakati_text'].dropna()
    wakati_texts = (row.split(" ") for row in df)
    for i, row in enumerate(wakati_texts):
        # .dropnaしたあとにi, 2などをすると、要素番号がずれてしまうので一致しない可能性がある。その対処
        # 正規化したあと、dfに書き込むために処理が必要
        df.iat[i, 2] = _normalize(_vector_sum(row, model))
    return df


def _vector_sum(row: List[str], model: Word2Vec) -> ndarray:
    '''
    引数rowの単語１つずつをベクトルに変換し、rowのベクトルの総和を求める
    params row: 1ツイートを形態素解析した単語のリスト
    params model: Word2Vecモデル
    return: numpy.ndarray
    '''
    word_vecs = (model.wv[word] for word in row)
    line_vec = zeros(word_vecs[0].shape, dtype=word_vecs[0].dtype)
    for word_vec in word_vecs:
        line_vec = line_vec + word_vec
    return line_vec


def _normalize(vec: ndarray) -> ndarray:
    '''
    ベクトルaのベクトルの正規化(単位ベクトルの計算)をする
    正規化で0と1の間の相対値が残る
    '''
    return vec / norm(vec)


if __name__ == "__main__":
    twitter_path = Path().cwd() / 'twitter'
    csv_path = twitter_path / 'a.csv'
    model_path = twitter_path / 'twitter.model'
    vector_path = twitter_path / 'b.csv'
    df_vector(csv_path, model_path).to_csv(vector_path)
