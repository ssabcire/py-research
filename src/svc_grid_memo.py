def _exec_grid():
    # スケーリング(データの前処理)))とSVMの2つのステップからなるパイプラインを構築
    # データのスケーリングは、データをSVMにわたす前に行うのが最適
    svm_est = Pipeline([('scaler', StandardScaler()), ('svc', SVC())])

    # RBFのパラメータであるCとgammaの値を1桁ずつ(対数的に)変化させる
    # パラメータをディクショナリにまとめることで、パラメータグリッドを作成.
    # SVMのパラメータグリッドのキー名はsvc__(SVMのパイプラインでの名前と2つのアンダースコア)で始まる。
    # その後に、等号(=)とSVCモデルのパラメータ名(c, gamma)を追加する。
    param_grid = dict(svc__C=[0.001, 0.01, 0.1, 1, 10, 100],
                      svc__gamma=[0.001, 0.01, 0.1, 1, 10, 100])
    # Pipeline と GridSearchCV を組み合わせて使うときは、パラメータ名の指定に工夫が必要になる。 具体的には <処理の名前>__<パラメータ名> という形式で指定する。

    # 交差検証用にデータ分割
    # 層化サンプリングとシャッフルを行う。n_splitsパラメータは、データセットのサンプリング(分割)の回数を指定
    # test_sizeパラメータは、フォールドのうちテストのために残しておくデータの割合または量を指定。
    # このモデルのスコアは、各フォールドのテストデータセットを使って計算
    cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=7)
    # グリッドサーチではなくランダムサーチを行う場合
    # rand_grid = RandomizedSearchCV(
    #     svm_est, param_distributions=param_grid, cv=cv, n_iter=10)

    # 単純な交差検証では、フォールドの数を表す整数をcvに割り当てる
    # クロスバリデーションの分割数
    # cv = 5

    # グリッドサーチインスタンス生成
    return GridSearchCV(svm_est, param_grid=param_grid, cv=cv)
