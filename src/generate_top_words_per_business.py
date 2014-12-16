from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONValueProtocol
from itertools import izip
from operator import itemgetter, attrgetter
import itertools
import re
import nltk
from nltk.corpus import stopwords, words


class TopWordsPerBusiness(MRJob):
	INPUT_PROTOCOL = JSONValueProtocol
	
	def mapper(self, _, review):
		if review['type'] == 'review':
			review_text = review['text']
			rating = review['stars']
			yield review['business_id'], (rating, review_text)

	def combiner(self, business_id, review_text):
		ratings, review_texts = izip(*review_text)

		review_words = dict()
		for review_text in review_texts:
			review_text = review_text.lower()
			word_list = re.findall('\w+', review_text)
						
			words = list(set(word_list) - set(nltk.corpus.stopwords.words('english')))
			
			for word in words:
				if word not in review_words:
					review_words[word] = 1
				else:
					review_words[word] += 1
		
		x = itertools.islice(sorted(review_words.items(), key=itemgetter(1), reverse=True), 0, 10)

		list_of_top_words = []
		for key, value in x:
		    list_of_top_words.append((key, value))
		
		yield business_id, list_of_top_words

	def reducer(self, key, value):
		yield key, list(value)

	def steps(self):
		return [MRStep(mapper=self.mapper,
						combiner=self.combiner,
						reducer=self.reducer)]

if __name__ == '__main__':
	TopWordsPerBusiness.run()