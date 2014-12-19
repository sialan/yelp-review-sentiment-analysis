from gensim import corpora, models
import numpy as np
from os import path

NUM_TOPICS = 25


class Corpus(object):
    def __init__(self, cursor, reviews_dictionary, corpus_path):
        self.cursor = cursor
        self.reviews_dictionary = reviews_dictionary
        self.corpus_path = corpus_path

    def __iter__(self):
        self.cursor.rewind()
        for review in self.cursor:
            yield self.reviews_dictionary.doc2bow(review["words"])

    def serialize(self):
        BleiCorpus.serialize(self.corpus_path, self, id2word=self.reviews_dictionary)
        return self

class Dictionary(object):
    def __init__(self, cursor, dictionary_path):
        self.cursor = cursor
        self.dictionary_path = dictionary_path

    def build(self):
        self.cursor.rewind()
        dictionary = corpora.Dictionary(review["words"] for review in self.cursor)
        dictionary.filter_extremes(keep_n=10000)
        dictionary.compactify()
        corpora.Dictionary.save(dictionary, self.dictionary_path)

        return dictionary

class Train:
    def __init__(self):
        pass

    @staticmethod
    def run(lda_model_path, corpus_path, num_topics, id2word):
        corpus = corpora.BleiCorpus(corpus_path)
        lda = gensim.models.LdaModel(corpus, num_topics=num_topics, id2word=id2word)
        lda.save(lda_model_path)

        return lda

if __name__ == '__main__':
    # Check that data exists
    dictionary_path = "models/dictionary.dict"
    corpus_path = "models/corpus.lda-c"
    lda_num_topics = 25
    lda_model_path = "models/lda_model_50_topics.lda"

    if not path.exists('../data/corpora/ap/ap.dat'):
        print('Error: Expected data to be present at ../data/corpora/ap/')
        print('Please cd into ../data/corpora/ & run ./download_ap.sh')
    
    # Load the data
    corpus = corpora.BleiCorpus('../data/corpora/ap/ap.dat', '../data/corpora/ap/vocab.txt')
    
    model = models.ldamodel.LdaModel(
        corpus, num_topics=NUM_TOPICS, id2word=corpus.id2word, alpha=None)
    
    ti = 0
    # Iterate over all the topics in the model
    for ti in xrange(model.num_topics):
        words = model.show_topic(ti, 64)
        tf = sum(f for f, w in words)
        with open('topics.txt', 'w') as output:
            output.write('\n'.join('{}:{}'.format(w, int(1000. * f / tf)) for f, w in words))
            output.write("\n\n\n")
    
    # We first identify the most discussed topic, i.e., the one with the
    # highest total weight
    
    # First, we need to sum up the weights across all the documents
    weight = np.zeros(model.num_topics)
    for doc in corpus:
        for col, val in model[doc]:
            weight[col] += val
            # As a reasonable alternative, we could have used the log of val:
            # weight[col] += np.log(val)
    
    max_topic = weight.argmax()
    
    # Get the top 64 words for this topic
    # Without the argument, show_topic would return only 10 words
    words = model.show_topic(max_topic, 25)