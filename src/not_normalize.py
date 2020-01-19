from pathlib import Path
from gensim.models.word2vec import Word2Vec
from pandas import read_csv, DataFrame, Series
from numpy import zeros


def f(csv_path, model_path, columns):
    model = Word2Vec.load(model_path)
    df = read_csv(csv_path).dropna()
    init_df = DataFrame(columns=columns)
    texts = df['text'].values.tolist()
    for i, row in enumerate(row.split(" ") for row in df['wakati_text']):
        vector = _vector_sum(row, model).astype('str')
        if vector is None:
            continue
        init_df = init_df.append(
            # Series([texts[i], " ".join(vector)], index=columns),
            Series([df['label'][i], texts[i], ' '.join(row), " ".join(vector)],
                   index=columns),
            ignore_index=True
        )
    return init_df


def _vector_sum(row, model):
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


if __name__ == "__main__":
    cwd = Path().cwd() / 'data'
    csv_path = cwd / 'trend-グレタさん-validLabel.csv'
    model_path = cwd / 'w2vallTweets' / "trend-グレタさん-allTweets.model"
    vector_path = cwd / 'trend-グレタさん-notNormalize.csv'
    columns = ['label', 'text', 'wakati_text', 'vector']
    f(csv_path, str(model_path), columns).to_csv(vector_path, index=False)
