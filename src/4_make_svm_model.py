import pickle
from pathlib import Path
from pandas import read_csv
from sklearn.svm import SVC
from sklearn.model_selection import (train_test_split, GridSearchCV,
                                     StratifiedShuffleSplit)


def run_svm(csv_path):
    df = read_csv(csv_path).dropna()
    # X = CountVectorizer().fit_transform(df(csv_path)['wakati-tweet'])
    X = [row.split(" ") for row in df['vector']]
    y = df['label']

    # もしかしたらここいらない可能性あり。理由は、StratifiedShuffleSplitする必要があるから
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=7, stratify=y)

    gscv = GridSearchCV(
        SVC(),
        param_grid={'C': [0.001, 0.01, 0.1, 1, 10, 100],
                    'gamma': [0.001, 0.01, 0.1, 1, 10, 100]},
        cv=StratifiedShuffleSplit(n_splits=10, test_size=0.2, random_state=7)
    )
    # ここもgscv.fit(X, y)でいいと思う
    gscv.fit(X_train, y_train)
    print(gscv.best_estimator_)
    print()
    print(gscv.best_params_)
    print()
    print(gscv.best_index_)
    print()
    print(gscv.best_score_)
    # # 以下考慮必要あり
    # return gscv.best_estimator_


if __name__ == "__main__":
    cwd_data = Path().cwd() / 'data'
    # ラベルが振ってある教師データを読み込みたい
    csv_path = '/Users/ssab/py/research/data/trend-死刑求刑-valid_label.csv'
    run_svm(csv_path)

    # save_path = cwd_data / "clf.pickle"
    # # ここ、最適なモデルを保存するようにしたい
    # pickle.dump(run_svm(csv_path), open(save_path, "wb"))
