import json
import re


def extract_text(filenames):
    texts = list()  # listでOK?
    for filename in filenames:
        f = open(filename, 'r')
        tweet_text = json.load(f)['full_text']
        text = re.sub(
            r'(https?://[\w/:%#\$&\?\(\)~\.=\+\-]+)|(RT@.*?:)|([ |　])',
            '',
            tweet_text
        )
        texts.append(text)
        f.close()
    return texts
