from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from .text import make_dataframe


def main():
    df = make_dataframe()
    features, vocab = vectorize(df['tweets'])
    # labels_train = n割のトレーニングのラベル. featuresは10割
    # ここで学習済みクラス分類モデルを作成。これにテストデータを渡して予測する
    y = df['labels']
    # X=特徴行列(説明変数), y=正解ラベル(目的変数)
    X_train, X_test, y_train, y_test = train_test_split(
        features, y, test_size=0.2, random_state=7, stratify=y)
    model = make_model(X_train, y_train)

    # テストデータで特徴量生成
    features_test = vectrize_using_vovab('<テスト用データ>', vocab)
    # 学習済みモデルに予測させる
    predicteds = classify(features_test, model)
    print(predicteds)  # predictedsには予測値が入る


def vectorize(corpus):
    '''
    コーパスを学習し、用語-文書の行列にする
    params corpus: 分かち書きされた文書s
    return: 用語-文書の行列の行列 type: array
    '''
    vectorizer = CountVectorizer()
    return vectorizer.fit_transform(corpus), vectorizer.vocabulary_


def vectrize_using_vovab(corpus, vocab):
    '''
    コーパスを学習し、用語-文書の行列にする。 また、引数のボキャブラリを使用
    params corpus: 分かち書きされた文書s
    return: 用語-文書の行列の行列 type: array
    '''
    vectorizer = CountVectorizer(vocabulary=vocab)
    return vectorizer.fit_transform(corpus)


def make_model(X, y):
    '''
    トレーニングデータにしたがってモデルを作成
    params X: 訓練(学習)用データのベクトル
    params y: 訓練(学習)用データのラベル
    return: モデル type: Object
    '''
    # パラメータ指定なし
    return svm.LinearSVC().fit(X, y)
    # モデルの種類やパラメータを何種類か試して、最も高い精度が出るものを採用するのが良い


def classify(X, model):
    '''
    predictでfeaturesがどこに分類されるかを予測し、分類結果を返す
    params X: テスト用データのベクトル
    return: ラベルの予測値 type: array
    '''
    return model.predict(X)


# accurancy_score(y_test, y_pred)で、予測値と実際の値を測定
