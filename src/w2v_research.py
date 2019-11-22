from pathlib import Path
from gensim.models.word2vec import Word2Vec
from numpy import zeros, ndarray
from numpy.linalg import norm
from pandas import read_csv, DataFrame


def df_vector(csv_path: Path, model_path: Path) -> DataFrame:
    '''
    DataFrameのwakati_textを1行ずつ単語ベクトルの総和を求める
    総和をDataFrameに追加
    '''
    # 一応tolist()使わなくてもいいか試してみること
    df = read_csv(csv_path)['wakati_text'].dropna()
    # .dropnaしたあとにi, 2などをすると、要素番号がずれてしまうので一致しない可能性がある。その対処
    wakati_texts = (row.split(" ") for row in df)
    model = Word2Vec.load(model_path)
    for i, row in enumerate(wakati_texts):
        # .dropnaしたあとにi, 2などをすると、要素番号がずれてしまうので一致しない可能性がある。その対処
        df.iat[i, 2] = _normalize(_vector_sum(row, model))
    return df


def _vector_sum(row: list, model: Word2Vec) -> ndarray:
    '''
    引数rowの要素１つずつをベクトルに変換し、rowのベクトルの総和を求める
    row: 1ツイートを形態素解析した単語のリスト
    model: Word2Vecモデル
    '''
    word_vecs = (model.wv[word] for word in row)
    # これと下のコメントアウト、結果が同じなのか気になる。
    # あと、np.sumの第1引数がiterableでない気がするので、動くか不明
    line_vec = zeros(word_vecs[0].shape, dtype=word_vecs[0].dtype)
    for word_vec in word_vecs:
        # ベクトルの総和を求める。他にいい感じでかけそう
        line_vec = line_vec + word_vec
    return line_vec


def _normalize(vec: ndarray) -> ndarray:
    '''
    ベクトルaのベクトルの正規化(単位ベクトルの計算)をする
    正規化で0と1の間の相対値が残る
    '''
    return vec / norm(vec)


# def _all_normalize2(vec):
    # from sklearn.preprocessing import StandardScaler
#     '''
#     標準化、これでもできないかな？
#     一応、ベクトルデータ全てに対して標準化を行うので注意
#     '''
#     return StandardScaler().fit_transform(vec)


if __name__ == "__main__":
    twitter_path = Path().cwd() / 'twitter'
    csv_path = twitter_path / 'a.csv'
    model_path = twitter_path / 'twitter.model'
    vector_path = twitter_path / 'b.csv'
    df_vector(csv_path, model_path).to_csv(vector_path)
