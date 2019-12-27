from pathlib import Path
from pandas import read_csv
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit
from sklearn.feature_extraction.text import CountVectorizer


def run_svm(csv_path, w2v=True, num=440):
    df = read_csv(csv_path).dropna()
    if w2v is True:
        # 特徴量にW2V
        X = [row.split(" ") for row in df['vector']][:num]
    else:
        # 特徴量にBoW
        X = CountVectorizer().fit_transform(
            [row for row in df['wakati_text']][:num])
    y = df['label'][:num]

    clf = GridSearchCV(
        SVC(),
        param_grid={'C': [0.001, 0.01, 0.1, 1, 10, 100],
                    'gamma': [0.001, 0.01, 0.1, 1, 10, 100]},
        cv=StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=5)
    )

    clf.fit(X, y)
    print(clf.best_score_)
    # print(clf.best_estimator_)
    # print(clf.best_params_)


if __name__ == "__main__":
    p_data = Path().cwd() / 'data'
    csv_path = p_data / 'trend-グレタ-label-vector.csv'
    for num in (40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440):
        run_svm(csv_path, True, num)
    print()
    for num in (40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440):
        run_svm(csv_path, False, num)

    # print()
    # for num in (50, 100, 150, 200, 250, 300, 350, 400, 440):
    #     run_svm(csv_path, True, num)
    # print()
    # for num in (50, 100, 150, 200, 250, 300, 350, 400, 440):
    #     run_svm(csv_path, False, num)
