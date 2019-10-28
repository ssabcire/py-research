from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from .text import make_dataframe


def run_svm():
    df = make_dataframe()
    # X=特徴行列(説明変数), y=正解ラベル(目的変数)
    X = _vectorize(df['tweets'])
    y = df['labels']
    # データ分割
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=7, stratify=y)
    # モデル作成
    model = _make_model(X_train, y_train)
    # 学習済みモデルにテストを予測させる
    y_pred = _classify(X_test, model)
    # 予測値とテスト用データの値を比較し、正しく分類されたサンプルの割合値を返す
    print(accuracy_score(y_test, y_pred))


def _vectorize(corpus):
    '''
    コーパスを学習し、用語-文書の行列にする
    params corpus: 分かち書きされた文書s
    return: 用語-文書の行列の行列、特徴量 type: array
    '''
    vectorizer = CountVectorizer()
    return vectorizer.fit_transform(corpus)


def _make_model(X, y):
    '''
    トレーニングデータにしたがってモデルを作成
    params X: 訓練(学習)用データのベクトル
    params y: 訓練(学習)用データのラベル
    return: モデル type: Object
    '''
    # パラメータ指定なし
    return svm.LinearSVC().fit(X, y)
    # モデルの種類やパラメータを何種類か試して、最も高い精度が出るものを採用するのが良い


def _classify(X, model):
    '''
    predictでfeaturesがどこに分類されるかを予測し、分類結果を返す
    params X: テスト用データのベクトル
    return: ラベルの予測値 type: array
    '''
    return model.predict(X)


if __name__ == '__main__':
    run_svm()
