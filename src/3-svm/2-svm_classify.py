import pickle
from pathlib import Path
from pandas import read_csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def test_classify(csv_path: Path, clf):
    '''
    予測性能を測る
    '''
    df = read_csv(csv_path).dropna()
    X = CountVectorizer().fit_transform(df['tweets'])
    # X = df['vectors']     #word2vec.version
    y = df['labels']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=7, stratify=y)

    y_pred = clf.predict(X_test)
    print(accuracy_score(y_test, y_pred))


def classify(csv_path: Path, clf):
    '''
    未分類のものも実際に分類し、ファイルにラベルを書き込む
    '''
    df = read_csv(csv_path).dropna()
    X = CountVectorizer().fit_transform(df['wakati-tweet'])
    # X = df['vectors']     #word2vec.version

    y_pred = clf.predict(X)
    writer(X, y_pred)


def writer(csv_path: Path, X, y_pred):
    d = dict()
    for x, y in zip(X, y_pred):
        d[x] = y
    # to_csv(d) てきな感じでやりたい


if __name__ == "__main__":
    twitter_path = Path().cwd() / 'twitter'
    csv_path = twitter_path / 'a.csv'

    with open("clf.pickle", "rb") as f:
        clf = pickle.load(f)
        classify(csv_path, clf)
