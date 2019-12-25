from pathlib import Path
from gensim.models.word2vec import Word2Vec


model_path = '/Users/ssab/py/research/data/trend-グレタさん-new.model'

model = Word2Vec.load(model_path)
print(model.wv.index2entity)
# print(model.wv.most_similar(positive=['反対'], topn=1000))
# print(model.wv.most_similar_to_given('死刑', ['みる', '内容', '目的', '求刑']))
# print(model.wv.similarity('', ''))
