# SVM + Word2Vec で分類

trend-グレタ-label-vector.csv 有効ラベルのみで学習


## 手順

1. 1_csv.processing.pyで作成
2. ラベルをつける
3. 4_a.pyでラベルが1, -1のもののみを抜き出し、新しいCSV作成
4. 2_make_model.pyで、3で作成したCSVからモデル作成
5. 3_vector.pyでvector作成し、新しいCSV作成
6. make_svm_model.pyで検証