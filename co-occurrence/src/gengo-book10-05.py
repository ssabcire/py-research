# 作成した正解データを読み込んでモデルを学習するプログラム
if __name__ == '__main__':
    # ラベル付きデータを読み込む
    # ...
    # 学習データ特徴量生成
    num_train = int(len(sentences) * 0.8)
    sentences_train = sentences[:num_train]
    labels_train = labels[:num_train]
    features, vocab = mlclassifier.convert_into_features(sentences_train)

    # 学習
    time_s = time.time()
    print(':::TRAIN START')
    model = mlclassifier.train(labels_train, features)
    print(':::TRAIN FINISHED', time.time() - time_s)

    # 学習モデルをファイルに保存
    joblib.dump(model, 'result/model.pkl')
    joblib.dump(vocab, 'result/vocab.pkl')

    # 分類の実行
    features_test = mlclassifier, convert_into_features_using_vocab(
        sentences[num_train:], vocab)      # テスト(評価)用データの特徴量(ベクトル)にする
    predicteds = mlclassifier.classify(features_test, model)  # 学習済みモデルを用いて分類
