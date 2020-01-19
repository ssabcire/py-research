from pathlib import Path
from pandas import read_csv
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit
from sklearn.feature_extraction.text import CountVectorizer


def run_svm(csv_path: Path, w2v=True):
    '''
    SVMで分類を行う
    '''
    df = read_csv(csv_path).dropna()
    if w2v is True:
        # 特徴量にW2V
        X = [row.split(" ") for row in df['vector']]
    else:
        # 特徴量にBoW
        cv = CountVectorizer()
        X = cv.fit_transform([row for row in df['wakati_text']])
        print(len(cv.get_feature_names()))
    y = df['label']

    clf = GridSearchCV(
        SVC(),
        param_grid={'C': [0.001, 0.01, 0.1, 1, 10, 100],
                    'gamma': [0.001, 0.01, 0.1, 1, 10, 100]},
        cv=StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=5)
    )

    clf.fit(X, y)
    print(clf.best_score_)
    return clf.best_score_


if __name__ == "__main__":
    cwd = Path().cwd() / 'data'
    csv_path = cwd / 'trend-グレタさん-validVector.csv'

    # ラベルがつけられたツイートのみで学習, W2V
    a = run_svm(csv_path, True)
    # ラベルがつけられたツイートのみで学習, BoW
    b = run_svm(csv_path, False)
    # print(b-a)
