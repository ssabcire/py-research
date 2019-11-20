from pandas import read_csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import (train_test_split, GridSearchCV,
                                     StratifiedShuffleSplit)


def run_svm(csv_path):
    df = read_csv(csv_path)
    # X=特徴行列(説明変数), y=正解ラベル(目的変数)
    # こちら、CountVectorizerではなく別のものを使いたいよね。
    # あと、文章の意味を持たせるために妥協してWord2Vec使うくらいで終わってもいいよね。
    X = CountVectorizer().fit_transform(df['tweets'])
    # X = df['vectors']     #word2vec.ver
    y = df['labels']
    # データ分割
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=7, stratify=y)
    grid_cv = GridSearchCV(
        SVC(),
        param_grid={'C': [0.001, 0.01, 0.1, 1, 10, 100],
                    'gamma': [0.001, 0.01, 0.1, 1, 10, 100]},
        cv=StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=7)
    )
    # 精度がいいモデルを取得 clf = classification
    best_clf = grid_cv.best_estimator_
    # 最も制度がいいモデルのスコア
    print('clf.best_score_', clf.best_score_)  # clf.best_score_ 0.98
    # モデル適合
    grid_cv.fit(X_train, y_train)
    # 予測値生成
    y_pred = grid_cv.predict(X_test)
    print(accuracy_score(y_test, y_pred))
    # 精度が良かったモデルの保存
    pickle.dump(clf.best_estimator_, open(filename, 'wb'))
#     # スコアの一覧を取得
#     gs_result = pd.DataFrame.from_dict(gscv.cv_results_)
#     gs_result.to_csv('gs_result.csv')

#   # 最高性能のモデルを取得し、テストデータを分類
#     best = gscv.best_estimator_
#     pred = best.predict(x_test)

#     # 混同行列を出力
#     print(confusion_matrix(y_test, pred))


if __name__ == "__main__":
    twitter_path = str(Path.home()) + "/py/research/twitter/"
    csv_path = twitter_path + 'a.csv'
    model_path = twitter_path + "twitter.model"
    run_svm(csv_name)
    # ここでモデルの保存をしたい。
    # s = pickle.dumps(clf) ????

    # もしモデルを読み込むとき
    # clf2 = pickle.loads(s)
