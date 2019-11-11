import numpy
from gensim.models.keyedvectors import KeyedVectors


def main():
    # モデル呼び出し
    model = KeyedVectors.load_word2vec_format(
        './vectors.bin', binary=True, unicode_errors='ignore')
    f = open('./community.owakati', 'r')
    # コミュニティ数分を回す
    for line in f:
        community_words = line.rstrip().split(' ')
        community_name = ''.join(community_words)
        try:
            # ベクトルの総和
            community_vec = text_to_vec(community_words, model)
            # 正規化
            community_vec = normalize(community_vec)
            # 保存
            numpy.savetxt('./vec/' + community_name, community_vec)
        except:
            pass


def text_to_vec(words, model):
    word_vecs = []
    for word in words:
        try:
            # 単語からベクトルを取得
            word_vecs.append(model[word])
        except:
            pass
    if len(word_vecs) == 0:
        return None
    text_vec = numpy.zeros(word_vecs[0].shape, dtype=word_vecs[0].dtype)
    for word_vec in word_vecs:
        # ベクトルの総和をとる
        text_vec = text_vec + word_vec
    return text_vec


def normalize(vec):
    return vec / numpy.linalg.norm(vec)


if __name__ == '__main__':
    main()


#-------------------------------------__#
# ここで、featuresとlabelを対応付けてファイルを作りたいよね
features = [ベクトルの総和の、コミュニティ数分のリスト]
label = [それに対応したラベル]

data_train, data_test, label_train, label_test = train_test_split(
    features, labels, test_size=0.1, random_state=1)

# トレーニングデータから分類器を作成 (Linear SVM)
estimator = LinearSVC(C=1.0)
estimator.fit(data_train, label_train)
# テストデータを分類器に入れる
label_predict = estimator.predict(data_test)
# Accuracy
print accuracy_score(label_test, label_predict)
