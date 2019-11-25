import pickle
from pathlib import Path
from pandas import read_csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import (train_test_split, GridSearchCV,
                                     StratifiedShuffleSplit)


def run_svm(csv_path):
    df = read_csv(csv_path).dropna()
    X = CountVectorizer().fit_transform(df(csv_path)['wakati-tweet'])
    # X = read_csv(csv_path)['vectors']     #word2vec.ver
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
    return gscv.best_estimator_


# clf = classification
if __name__ == "__main__":
    twitter_path = Path().cwd() / 'twitter'
    csv_path = twitter_path / 'a.csv'
    best_clf = run_svm(csv_path)
    best_clf.best_score_
    with open("clf.pickle", "wb") as f:
        pickle.dump(best_clf, f)
