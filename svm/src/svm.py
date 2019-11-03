from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from pandas import read_csv


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


if __name__ == "__main__":
    csv_name = 'a'
    run_svm(csv_name)
