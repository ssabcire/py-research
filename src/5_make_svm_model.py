from pathlib import Path
from pandas import read_csv
import re
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit
from sklearn.feature_extraction.text import CountVectorizer
from pyknp import Juman


def run_svm(csv_path):
    df = read_csv(csv_path).dropna()
    X = [row.split(" ") for row in df['vector']]    # 特徴量にW2V
    # X = cv(csv_path)                                # 特徴量にBoW
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


def cv(csv_path):
    df = read_csv(csv_path).dropna()
    cv = CountVectorizer()
    return cv.fit_transform(
        [' '.join(_morphological_analysis(row)) for row in df['text']])


def _morphological_analysis(row):
    '''
    tweetを形態素解析し、リストで返す
    '''
    text = _remove_unnecessary(row)
    if not text:
        return []
    return [mrph.genkei for mrph in Juman().analysis(text).mrph_list()
            if mrph.hinsi in ['名詞', '動詞', '形容詞', '接尾辞']]


def _remove_unnecessary(text):
    '''
    ツイートの不要な部分を削除
    '''
    # URL, 'RT@...:', '@<ID> '
    text = re.sub(
        r'(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)|(RT@.*?:)|(@(.)+ )',
        '', text
    )
    # ツイートがひらがな1,2文字しかない場合, 空白
    # [", #, @] はjumanが扱えない
    return re.sub(
        r'(^[あ-ん]{1,2}$)|([ |　])|([#"@])',
        '', text
    )


if __name__ == "__main__":
    p_data = Path().cwd() / 'data'
    csv_path = p_data / 'trend-グレタさん-valid_label.csv'
    run_svm(csv_path)
