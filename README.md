# SVM + Word2Vec で分類

## 手順

1. research 配下に twitter ディレクトリを作成、json データを配置
2. src/csv_processing.py のファイル名を書き換える
3. src/csv_processing.py 実行. json データを CSV に
4. src/w2v_research.py のファイル名を書き換える
5. src/w2v_research.py 実行 ベクトルを作成
6. src/make_svm_model.py のファイル名を書き換える
7. src/make_svm_model.py 実行 SVM モデルを作成
8. src/svm_classify.py ファイル名を書き換える
9. src/svm_classify.py 精度確認と分類
