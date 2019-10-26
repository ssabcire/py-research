from sklearn.feature_extraction.text import CountVectorizer
from text import morphological_analysis

morpho_list = list()
text1 = "私はラーメンが好き"
text2 = "私は餃子が好き"
text3 = "私はラーメンが嫌い"
morpho_list.append(' '.join(morphological_analysis(text1)))
morpho_list.append(' '.join(morphological_analysis(text2)))
morpho_list.append(' '.join(morphological_analysis(text3)))  # 3行4列の行列になる
cv = CountVectorizer()
# 特徴量に変換
features = cv.fit_transform(morpho_list)
vocab = cv.vocabulary_

# 次に、学習と分類を行う
# 学習はtrain(LinearSVC,)
# 分類はclassify(predict)
# テストデータと学習用データを分けるコードも書かないといけない


# matrix = cv.fit_transform(morpho_list) # 行列
# print(features.toarray())
# print(cv.get_feature_names())
# print(cv.vocabulary_)
