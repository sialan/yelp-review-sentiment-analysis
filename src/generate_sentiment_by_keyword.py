from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import re
from nltk.corpus import stopwords


def get_features(text):
	"""normalize words by lowercasing and dropping non-alpha characters"""
	norm = lambda word: re.sub('[^a-z]', '', word.lower())

	"""create a list of lowercase words from the input text, and remove empty strings"""
	words = list(norm(word) for word in text.split() if word != '')
	
	"""build a list of bigrams by pairing words in the text"""
	bigrams = zip(words[0::2],words[1::2])+zip(words[1::2],words[2::2])

	"""build a list of trigrams by pairing words in the text"""
	trigrams = zip(words[0::3],words[1::3],words[2::3])+zip(words[1::3],words[2::3],words[3::3])+zip(words[2::3],words[3::3],words[4::3])

	"""build a list of fourgrams by pairing words in the text"""
	fourgrams = zip(words[0::3],words[1::3],words[2::3])+zip(words[1::3],words[2::3],words[3::3])+zip(words[2::3],words[3::3],words[4::3])

	"""build a list of fivegrams by pairing words in the text"""
	fivegrams = zip(words[0::3],words[1::3],words[2::3])+zip(words[1::3],words[2::3],words[3::3])+zip(words[2::3],words[3::3],words[4::3])

	return words + bigrams + trigrams + fourgrams + fivegrams

def sentiment feature_extractor(words):
    """Default feature extractor for the NaiveBayesAnalyzer."""
    return dict(((word, True) for word in words))

class KeywordSentiment(MRJob):
	"""Extract features from each row(review) in the dataset."""

	# The input is a json key value pair. The key being null
    INPUT_PROTOCOL = JSONValueProtocol

    def mapper_init(self):
        neg_ids = nltk.corpus.movie_reviews.fileids('neg')
        pos_ids = nltk.corpus.movie_reviews.fileids('pos')
        neg_features = [(sentiment_feature_extractor(
            nltk.corpus.movie_reviews.words(fileids=[f])), 'neg') for f in neg_ids]
        pos_features = [(sentiment_feature_extractor(
            nltk.corpus.movie_reviews.words(fileids=[f])), 'pos') for f in pos_ids]
        train_data = neg_features + pos_features
        self.classifier = nltk.classify.NaiveBayesClassifier.train(train_data)

	def mapper(self, _, data):
		if data['type'] == 'review':
    		stars = data['stars']
    		text = data['text']
    
    		#get a list of features for each review
    		features = get_features(text)
    
    		yield data['review_id'], (stars, text, features)

	def combiner(self, review_id, features):
        stars = features[0]
        word_sentiment = {}
		for feature in features[2]:
			cleaned_features = sentiment_feature_extractor(feature)
            prob_dist = self.classifier.prob_classify(cleaned_features)
			for word in feature:
                if word in word_sentiment:
                    word_sentiment[word]['pos'] += prob_dist.prob('pos')
                    word_sentiment[word]['neg'] += prob_dist.prob('neg')}
                else:
                    word_sentiment[word] = {'pos': prob_dist.prob('pos'), 'neg': prob_dist.prob('neg')}

		yield review_id, (stars, word_sentiment)

	def reducer(self, review_id, features):
        # TODO: Fine tune sentiment analysis
        final_sentiment = {}
        for key, value in features[1].iteritems():
            if value['pos'] >= value['neg']:
                final_sentiment[key] = 'positive'
            else:
                final_sentiment[key] = 'negative'
		yield review_id, final_sentiment

	def steps(self):
		return [MRStep(mapper_init=self.mapper_init,
                        mapper=self.mapper,
                        combiner=self.combiner,
                        reducer=self.reducer)]

if __name__ == "__main__":
    KeywordSentiment.run()