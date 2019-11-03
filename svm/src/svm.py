from pandas import read_csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.model_selection import (train_test_split, GridSearchCV,
                                     StratifiedShuffleSplit)


def run_svm(csv_name):
    df = read_csv(csv_name, encoding="utf-8")
    # X=特徴行列(説明変数), y=正解ラベル(目的変数)
    X = CountVectorizer().fit_transform(df['tweets'])
    y = df['labels']
    # データ分割
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=7, stratify=y)
    # トレーニングデータにしたがってモデルを作成
    # パラメータ指定なし. モデルの種類やパラメータを何種類か試して、最も高い精度が出るものを採用するのが良い
    model = svm.LinearSVC().fit(X_train, y_train)
    # 学習済みモデルにテストを予測させる
    y_pred = model.predict(X_test)
    # 予測値とテスト用データの値を比較し、正しく分類されたサンプルの割合値を返す
    # predictでfeaturesがどこに分類されるかを予測し、分類結果を返す
    print(accuracy_score(y_test, y_pred))


def run_svm2():
    df = read_csv(csv_name, encoding="utf-8")
    # X=特徴行列(説明変数), y=正解ラベル(目的変数)
    X = CountVectorizer().fit_transform(df['tweets'])
    y = df['labels']
    # データ分割
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=7, stratify=y)
    grid_cv = grid()
    grid_cv.fit(X_train, y_train)
    svm_model = grid_cv.best_estimator_  # 多分こう？

    y_pred = svm_model.predict(X_test)
    print(accuracy_score(y_test, y_pred))


def grid():
    svm_est = Pipeline([('scaler', StandardScaler()), ('svc', SVC())])
    # RBFのパラメータであるCとgammaの値を1桁ずつ(対数的に)変化させる
    Cs = [0.001, 0.01, 0.1, 1, 10]
    gammas = [0.001, 0.01, 0.1, 1, 10]

    # パラメータをディクショナリにまとめることで、パラメータグリッドを作成.
    # SVMのパラメータグリッドのキー名はsvc__(SVMのパイプラインでの名前と2つのアンダースコア)で始まる。
    # その後に、等号(=)とSVCモデルのパラメータ名(c, gamma)を追加する。
    param_grid = dict(svc__C=Cs, svc__gamma=gammas)

    # 交差検証のスキームを指定
    # 層化サンプリングとシャッフルを行う。n_splitsパラメータは、データセットのサンプリング(分割)の回数を指定
    # test_sizeパラメータは、フォールドのうちテストのために残しておくデータの割合または量を指定。
    # このモデルのスコアは、各フォールドのテストデータセットを使って計算
    cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=7)

    # 単純な交差検証では、フォールドの数を表す整数をcvに割り当てる
    # クロスバリデーションの分割数
    cv = 10

    # グリッドサーチを実行
    grid_cv = GridSearchCV(svm_est, param_grid=param_grid, cv=cv)
    return grid_cv


if __name__ == "__main__":
    csv_name = 'a'
    run_svm(csv_name)
