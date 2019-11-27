from pathlib import Path
from pandas import read_csv, DataFrame, Series

'''
1, -1のラベルが振られたデータのみを抽出して、label, text, vectorのDFで保存
'''


def a(csv_path):
    df = read_csv(csv_path)
    init_df = DataFrame(columns=df.columns)
    for i, row in df.iterrows():
        if row['label'] in ["-1", "1"]:
            df = init_df.append(
                Series(row, index=df.columns), ignore_index=True)
    return init_df


if __name__ == "__main__":
    twitter_path = Path().cwd() / 'twitter'
    csv_path =
    valid_label_path =
    df = a(csv_path).dropna().to_csv(valid_label_path, index=False)
