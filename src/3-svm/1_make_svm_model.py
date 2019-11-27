import pickle
from pathlib import Path
from pandas import read_csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import (train_test_split, GridSearchCV,
                                     StratifiedShuffleSplit)


def run_svm(csv_path):
    df = read_csv(csv_path).dropna()
    # X = CountVectorizer().fit_transform(df(csv_path)['wakati-tweet'])
    X = [row.split(" ") for row in df['vectors']]  # word2vec.ver
    y = df['labels']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=7, stratify=y)

    gscv = GridSearchCV(
        SVC(),
        param_grid={'C': [0.001, 0.01, 0.1, 1, 10, 100],
                    'gamma': [0.001, 0.01, 0.1, 1, 10, 100]},
        cv=StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=7)
    )
    gscv.fit(X_train, y_train)
    # 以下考慮必要あり
    return gscv.best_estimator_


if __name__ == "__main__":
    twitter_path = Path().cwd() / 'twitter'
    # ラベルが振ってある教師データを読み込みたい
    csv_path = twitter_path / 'a.csv'
    # ここ、最適なモデルを保存するようにしたい
    pickle.dump(run_svm(csv_path), open("clf.pickle", "wb"))
