from textblob import TextBlob
from util.rake import Rake


def extract_top_keywords(review):
	rake = Rake("../data/corpora/SmartStoplist.txt")
	keywords = rake.run(review)
	return keywords

def extract_snippets_by_keyword(keywords_list, review):
	pass

def concatenate_all_reviews(reviews_list):
	combined = " ".join(reviews_list)
	return combined

def split_review_into_segments(review):
	b = TextBlob(review)
	return [str(x) for x in b.sentences]

def get_basic_ngrams(text):
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
