from gensim.models import Word2Vec

class MeanEmbeddingVectorizer(object):
    # 単語の分散表現の平均値を求めるクラスの定義
    # CountVectorizer()のように使うことができる
    def __init__(self, word2vec):
        self.word2vec = word2vec
        # テキストが空の場合、他のすべてのベクトルと同じ次元のゼロのベクトルを返す必要がある
        # ここ、iter省略できない?
        # self.dim = next(iter(word2vec.values())).size

    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array(
            [np.mean(
                [self.word2vec[w] for w in words if w in self.word2vec]
                or [np.zeros(self.dim)], axis=0)
             for words in X]
        )


class TfidfEmbeddingVectorizer(object):
    # TF-IDFで重み付けした分散表現を求めるクラスの定義
    # TfidfVectorizer()のように使うことができる
    def __init__(self, word2vec):
        self.word2vec = word2vec
        self.word2weight = None
        self.dim = word2vec.values()
        self.dim = next(iter(self.dim))
        self.dim = self.dim.size

    def fit(self, X, y):
        tfidf = TfidfVectorizer(analyzer=lambda x: x)
        tfidf.fit(X)
        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])

        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] * self.word2weight[w]
                     for w in words if w in self.word2vec] or
                    [np.zeros(self.dim)], axis=0)
            for words in X
        ])


# ベースラインとなる既存手法のモデルの準備
# etree
etree = Pipeline([("count_vectorizer", CountVectorizer(analyzer=lambda x: x)),
                  ("linear svc", SVC(kernel="linear"))])
# etreeのTF-IDF版
etree_tfidf = Pipeline([("tfidf_vectorizer", TfidfVectorizer(analyzer=lambda x: x)),
                        ("extra trees", ExtraTreesClassifier(n_estimators=200))])

# Word2Vecを特徴量としてExtraTreesによる分類器を準備する。
etree_w2v = Pipeline([("word2vec vectorizer", MeanEmbeddingVectorizer(w2v)),
                      ("extra trees", ExtraTreesClassifier(n_estimators=200))])

etree_w2v_tfidf = Pipeline([("word2vec vectorizer", TfidfEmbeddingVectorizer(w2v)),
                            ("extra trees", ExtraTreesClassifier(n_estimators=200))])


# 4点以上であれば1そうでなければ0
corpus_data["label"] = np.where(corpus_data.rating >= 4, 1, 0)

# scikit-learnで使う入力とラベルの設定
X, y = np.array(corpus_data.text_wakati), np.array(corpus_data.label)

sentences2 = [token.split(" ") for token in corpus_data.text_wakati]


# Word2Vecを実行する。
model = Word2Vec(sentences2,
                 size=100,
                 window=5,
                 min_count=5,
                 workers=2)
w2v = {w: vec for w, vec in zip(model.wv.index2word, model.wv.syn0)}
# ここ、model.wv

# 上の処理はこうするのがベストなはず
model = gensim.models.Word2Vec(X, size=100)
w2v = dict(zip(model.wv.index2word, model.wv.syn0))  # word: vector という形の辞書?
# そもそもWord2Vecの学習の仕方を知る必要があるかも

# 各モデルを実行し、クロスバリデーションスコアを計算し、出力させる。
all_models = [
    ("etree", etree),
    ("etree_tfidf", etree_tfidf),
    ("`w`2v", etree_w2v),
    ("w2v_tfidf", etree_w2v_tfidf)
]
scores = sorted([(name, cross_val_score(model, X, y, cv=5).mean())
                 for name, model in all_models],
                key=lambda x: x[0])
print(tabulate(scores, floatfmt=".4f", headers=("model", 'score')))

# 棒グラフでクロスバリデーションスコアを比較する。
plt.figure(figsize=(15, 6))
sns.barplot(x=[name for name, _ in scores], y=[score for _, score in scores])


# 各モデルを実行し、クロスバリデーションスコアを計算し、出力させる。
all_models = [
    ("etree", etree),
    ("etree_tfidf", etree_tfidf),
    ("w2v", etree_w2v),
    ("w2v_tfidf", etree_w2v_tfidf)
]
# mean=np.mean()
scores = sorted([(name, cross_val_score(model, X, y, cv=5).mean())
                 for name, model in all_models],
                key=lambda x: x[0])
print(tabulate(scores, floatfmt=".4f", headers=("model", 'score')))

# 棒グラフでクロスバリデーションスコアを比較する。
plt.figure(figsize=(15, 6))
sns.barplot(x=[name for name, _ in scores], y=[score for _, score in scores])
