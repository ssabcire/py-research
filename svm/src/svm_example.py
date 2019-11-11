model = Word2Vec(X, size=100, window=5, min_count=5, workers=2)
w2v = {w: vec for w, vec in zip(model.index2word, model.syn0)}

# ベースラインとなる既存手法のモデルの準備
mult_nb = Pipeline([("count_vectorizer", CountVectorizer(
    analyzer=lambda x: x)), ("multinomial nb", MultinomialNB())])
bern_nb = Pipeline([("count_vectorizer", CountVectorizer(
    analyzer=lambda x: x)), ("bernoulli nb", BernoulliNB())])
mult_nb_tfidf = Pipeline([("tfidf_vectorizer", TfidfVectorizer(
    analyzer=lambda x: x)), ("multinomial nb", MultinomialNB())])
bern_nb_tfidf = Pipeline([("tfidf_vectorizer", TfidfVectorizer(
    analyzer=lambda x: x)), ("bernoulli nb", BernoulliNB())])
svc = Pipeline([("count_vectorizer", CountVectorizer(
    analyzer=lambda x: x)), ("linear svc", SVC(kernel="linear"))])
svc_tfidf = Pipeline([("tfidf_vectorizer", TfidfVectorizer(
    analyzer=lambda x: x)), ("linear svc", SVC(kernel="linear"))])

# 単語の分散表現の平均値を求めるクラスの定義


class MeanEmbeddingVectorizer:
    def __init__(self, word2vec):
        self.word2vec = word2vec
        self.dim = self.next(iter(word2vec.values())).size

    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] for w in words if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for words in X
        ])

# TF-IDFで重み付けした分散表現を求めるクラスの定義


class TfidfEmbeddingVectorizer(object):
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


# Word2Vecを特徴量としてExtraTreesによる分類器を準備する。
etree_w2v = Pipeline([("word2vec vectorizer", MeanEmbeddingVectorizer(w2v)),
                      ("extra trees", ExtraTreesClassifier(n_estimators=200))])

etree_w2v_tfidf = Pipeline([("word2vec vectorizer", TfidfEmbeddingVectorizer(w2v)),
                            ("extra trees", ExtraTreesClassifier(n_estimators=200))])

# 各モデルを実行し、クロスバリデーションスコアを計算し、出力させる。
all_models = [
    ("mult_nb", mult_nb),
    ("mult_nb_tfidf", mult_nb_tfidf),
    ("bern_nb", bern_nb),
    ("bern_nb_tfidf", bern_nb_tfidf),
    ("svc", svc),
    ("svc_tfidf", svc_tfidf),
    ("w2v", etree_w2v),
    ("w2v_tfidf", etree_w2v_tfidf)
]
scores = sorted([(name, cross_val_score(model, X, y, cv=5).mean())
                 for name, model in all_models],
                key=lambda x: x[0])
print(tabulate(scores, floatfmt=".4f", headers=("model", 'score')))


# 棒グラフでクロスバリデーションスコアを比較する。
plt.figure(figsize=(15, 6))
sns.barplot(x=[name for name, _ in scores], y=[score for _, score in scores])
