# Twitterを用いたニュースに対する意見の分類
SVM+Word2Vec(and Bag of Words)で分類する

# 前提
すでにJSONファイルをTwitterフォルダに配置している

## 手順
1. 1_csv_processing.pyで、JSONファイルからCSVを作成(trend-グレタさん.csvを作成)
2. 1で作成したCSVに手作業でラベルをつける(trend-グレタさん-label.csvを作成)
3. 2_a.pyで、2でラベルをつけたCSVで1, -1のみがふられたラベルの行のみを抜き出す(trend-グレタさん-validLabel.csv)
4. 3_make_modelで、W2Vモデルを作成(trend-グレタさん-allTweets.model)
5. 4_vector.pyで、2でつくったCSVファイルにベクトルを追加して、新しくCSVファイルを作成(trend-グレタさん-validVector.csv)
6. 5_make_svm_model.pyでSVMを使って分類し、分類成功率を求める


## 開発環境
MacOS Catalina 10.15.3
