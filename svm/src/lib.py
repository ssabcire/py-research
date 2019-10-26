import csv
import json
from .text import morphological_analysis

# jsonfiles = glob()...

# ここargsで受け取りたいよね
csv_name = 'a'


def pre_processing():
    _write_to_csv(_load_tweet_from_file())


def _load_tweet_from_file(jsonfiles: list) -> list:
    tweets = list()
    for filename in jsonfiles:
        f = open(filename, 'r')
        tweets.append(json.load(f)['full_text'])
        f.close()
    return tweets


header = ["id", "text"]


def _write_to_csv(tweets):
    with open(csv_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(
            [[i+1, tweet] for i, tweet in enumerate(tweets)]
        )


def _write_to_csv_using_morpho(tweets):
    with open(csv_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(
            [[i, ' '.join(morphological_analysis(tweet))]
             for i, tweet in enumerate(tweets)]
        )


if __name__ == '__main__':
    pre_processing()
