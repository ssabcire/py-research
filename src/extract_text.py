import json
import re


def extract_text(filename):
    f = open(filename, 'r')
    tweet_text = json.load(f)['full_text']
    text = re.sub(
        r'(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)|(RT@.*?:)|([ |　])',
        '',
        tweet_text
    )
    f.close()
    return text
