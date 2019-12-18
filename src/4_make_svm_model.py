# import pickle
from pathlib import Path
from pandas import read_csv
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit


def run_svm(csv_path):
    df = read_csv(csv_path).dropna()
    X = [row.split(" ") for row in df['vector']]
    y = df['label']

    clf = GridSearchCV(
        SVC(),
        param_grid={'C': [0.001, 0.01, 0.1, 1, 10, 100],
                    'gamma': [0.001, 0.01, 0.1, 1, 10, 100]},
        cv=StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
    )

    clf.fit(X, y)
    print(clf.best_estimator_)
    print(clf.best_params_)
    print(clf.best_score_)


if __name__ == "__main__":
    p_data = Path().cwd() / 'data'
    csv_path = p_data / 'trend-死刑求刑-valid_label.csv'
    run_svm(csv_path)
