from pathlib import Path
from pandas import read_csv
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit
from sklearn.feature_extraction.text import CountVectorizer
from pyknp import Juman


def run_svm(csv_path):
    df = read_csv(csv_path).dropna()
    # X = [row.split(" ") for row in df['vector']]    # 特徴量にW2V
    # BoW
    X = CountVectorizer().fit_transform(row for row in df['wakati_text'])
    y = df['label']

    clf = GridSearchCV(
        SVC(),
        param_grid={'C': [0.001, 0.01, 0.1, 1, 10, 100],
                    'gamma': [0.001, 0.01, 0.1, 1, 10, 100]},
        cv=StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=5)
    )

    clf.fit(X, y)
    print(clf.best_estimator_)
    print(clf.best_params_)
    print(clf.best_score_)


if __name__ == "__main__":
    p_data = Path().cwd() / 'data'
    csv_path = p_data / 'trend-グレタ-label-vector.csv'
    run_svm(csv_path)
