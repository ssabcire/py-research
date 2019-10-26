# とりあえず、BoWでもいいのでSVM完成させておきたい...

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn import svm
from .text import extract_text, morphological_analysis


def xlsx_in(df, file_name, sheet_name):
    '''
    データフレーム化したツイートデータをxlsxファイルとして出力
    '''
    #     df_sample = pd.read_excel(
    #     '/Users/ssab/Desktop/product/tweet_data/modelData3_plus2.xlsx',
    #     sheet_name='testdata sheet'
    # )
    # # 0以外?どゆこと?df_sample['score'] != 0じゃないし...
    # df_np = df_sample[df_sample != 0]
    # df_np.dropna(inplace=True)
    # return dfをしたい


def xlsx_out(df, file_name, sheet_name):
    '''
    データフレーム化したツイートデータをxlsxファイルとして出力
    '''

    excel_writer = pd.ExcelWriter(file_name)  # 出力するファイルを指名
    df.to_excel(excel_writer, sheet_name)  # シート名を指定しdfを書き出し
    excel_writer.save()


def create_dataframe(text_column_name, text, params_column_name, Params):
    '''
    tweet本文のリストをデータフレーム化して返す
    params text_column_name : text列の名前
    text : ツイート本文のリスト
    params_column_name : Params列の名前
    Params : 数字のリスト
    '''
    # idx = [i for i in range(len(text))]
    df = pd.DataFrame({text_column_name: text, params_column_name: Params})
    # {text_column_name: text, params_column_name: Params}, index=idx)
    return df


def a():
    '''
    出現する単語のカウントを特徴量にする?
    CountVectorizer=素性ベクトル?
    '''
    #     feature_vectors: scipy.sparse の csr_matrix 形式
    cv = CountVectorizer()
    # feature_vectors: scipy.sparse の csr_matrix 形式
    feature_vectors = cv.fit_transform(   # ベクトル化
        mwl.get_wakati_list(df_np['tweet'], 'off'))  # ここ、引数にリスト受け取ってるので注意
    # 列要素(単語) 名 feature_integerインデックスからfeature_nameを求める。リスト
    feature_names = cv.get_feature_names()
    # vocabulary = count_vectorizer.get_feature_names()

    # svm 学習      # 探索するパラメータを設定 # ハイパーパラメータ 最適な値を求めるにはランダムサーチ
    svm_tuned_parameters = [{     # カーネル法
        'kernel': ['rbf'],                      # RBFカーネルを用いる
        'gamma': [2**n for n in range(-15, 3)],  # rbfの直径の大きさ
        'C': [2**n for n in range(-5, 15)]      # 正則化パラメータ
    }]

    # グリッドサーチCountVectrizer
    gscv = GridSearchCV(                            # インスタンス化
        svm.SVC(),
        svm_tuned_parameters,
        cv=5,      # クロスバリデーションの分割数
        n_jobs=1,  # 並列スレッド数
        verbose=3  # 途中結果の出力レベル 0 だと出力しない
    )

    # インスタンスgscvで、モデルを適合。第2引数にはネガポジのスコアをリストで渡す
    gscv.fit(feature_vectors, list(df_np['score']))
    # 最適なパラメータを代入
    svm_model = gscv.best_estimator_


# svm 分類
def get_feature_vectors(words, feature_names) -> dict:
    '''
    ネガポジ判定したwakati_listとそれに対応したネガポジのスコアを取得する
    '''
    # 出現する単語のカウントを特徴量にする。
    count_vectorizer = CountVectorizer(vocabulary=feature_names)
    # 特徴量をベクトル化
    feature_vectors = count_vectorizer.fit_transform(words)

    return dict(words=words, fv=feature_vectors)

#----------------------------------------------------------------------#


def _run_svm():
    # 訓練データをAから読み込む
    df = pd.read_excel('allTweet_2.xlsx', sheetname='AllTweet_sheet')
    df.dropna(inplace=True)

    # dfのtweet列を取り出す
    # wakati_list = mwl.get_wakati_list(df['tweet'], 'on')
    words_list = list()
    for tweet in df['tweet']:
        words_list.append(morphological_analysis(extract_text(tweet)))
    # ネガポジのスコアを取得
    res_t = get_feature_vectors(words_list)

    # インデックス/特徴量ベクトル/1ツイートの形態素解析されたツイートでdataFrameを作る
    df_res = cdx.create_dataFrame(text_column_name='sliced_tweet', text=res_t['wl'],
                                  params_column_name='feature_vectors', Params=list(svm_model.predict(res_t['fv'])))
    # ここ、wkatisではなくwlなのでは？   key=wlを使ってwakati_listの値を取り出す
    # df_res = cdx.create_dataFrame(text_column_name='sliced_tweet', text=res_t['wkatis'],
    #   params_column_name='feature_vectors', Params=list(svm_model.predict(res_t['fv'])))
    # cdx.xlsx_out(df_res, 'pn_tweet.xlsx', 'pn_tweet_sheet')
# if __name__ == '__main__':
#         run_svm()
