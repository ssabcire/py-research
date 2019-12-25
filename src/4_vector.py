from pathlib import Path
from gensim.models.word2vec import Word2Vec
from typing import List
from numpy import zeros, ndarray
from numpy.linalg import norm
from pandas import read_csv, DataFrame, Series


def df_vector(csv_path, model_path: str, columns: List[str]) -> DataFrame:
    '''
    Word2Vecのモデルを使って、新しく
    ['label', 'text', 'wakati_text', 'vector']のDataFrameを作成する
    '''
    model = Word2Vec.load(model_path)
    df = read_csv(csv_path).dropna()
    init_df = DataFrame(columns=columns)
    texts = df['text'].values.tolist()
    # wakati_texts = (row.split(" ") for row in df['wakati_text'])
    for i, row in enumerate(row.split(" ") for row in df['wakati_text']):
        vector = _vector_sum(row, model)
        if vector is None:
            continue
        vector = _normalize(vector).astype('str')
        init_df = init_df.append(
            # Series([texts[i], " ".join(vector)], index=columns),
            Series([df['label'][i], texts[i], ' '.join(row), " ".join(vector)],
                   index=columns),
            ignore_index=True
        )
    return init_df


def _vector_sum(row: List[str], model: Word2Vec) -> ndarray:
    '''
    引数rowの単語１つずつをベクトルに変換し、rowのベクトルの総和を求める
    params row: 1ツイートを形態素解析した単語のリスト
    params model: Word2Vecモデル
    return: numpy.ndarray
    '''
    word_vecs = list()
    for word in row:
        try:
            word_vecs.append(model.wv[word])
        except KeyError:
            pass
    if not word_vecs:
        return None
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
    p_data = Path().cwd() / 'data'
    csv_path = p_data / 'trend-グレタ-label-notVector.csv'
    model_path = p_data / "trend-グレタさん-new.model"
    vector_path = p_data / 'trend-グレタ-label-vector.csv'
    columns = ['label', 'text', 'wakati_text', 'vector']
    df_vector(csv_path, str(model_path), columns
              ).to_csv(vector_path, index=False)
