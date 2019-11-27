from pathlib import Path
from gensim.models.word2vec import Word2Vec


twitter_path = str(Path.home()) + "/py/research/twitter/"
model_path = twitter_path + "trend-死刑求刑.model"

model = Word2Vec.load(model_path)
# print(model.wv.index2entity)
print(model.wv.most_similar(positive=['反対'], topn=1000))
# print(model.wv.similarity('', ''))
