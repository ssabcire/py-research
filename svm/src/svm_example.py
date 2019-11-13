class MeanEmbeddingVectorizer:
    # 単語の分散表現の平均値を求めるクラスの定義
    def __init__(self, word2vec):
        self.word2vec = word2vec
        # ここ、なんなんだ...?
        self.dim = next(iter(word2vec.values())).size


# モデルを読み込む
model = load()
w2v = {w: vec for w, vec in zip(model.wv.index2entity, model.wv.syn0)}

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
