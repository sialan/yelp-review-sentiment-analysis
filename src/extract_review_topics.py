import pandas as pd
import gensim
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords, words
from nltk.stem import PorterStemmer, SnowballStemmer

from features import split_review_into_segments

results = {}

business_data = pd.read_csv('./data/yelp/yelp_academic_dataset_business.csv', index_col = 'business_id')
review_data = pd.read_csv('./data/yelp/yelp_academic_dataset_review.csv', index_col = ('review_id', 'business_id'))
porter_stemmer = PorterStemmer()
snowball_stemmer = SnowballStemmer('english')

# iterate through each business
for business_id, business_row_data in business_data.head(100).iterrows():
    results[business_id] = {}
    
    # train topic model
    combined = " || ".join(review_data[review_data.index.get_level_values(1) == business_id].text.values.tolist())
    # what are the topics

    # iterate through all reviews for business
    for review_id, business_review_data in review_data[review_data.index.get_level_values(1) == business_id].iterrows():
        b = TextBlob(business_review_data.text)
        try:
            # cleaned = porter_stemmer.stem(business_review_data.text)
            cleaned_tokens = [snowball_stemmer.stem(x) for x in b.words]
            cleaned = " ".join(cleaned_tokens)
        except:
            cleaned = b
        
        # go through each sentence and split it predict a topic for each
        keywords = rake.run(cleaned)

        for topic in keywords:
            polarity = topic.sentiment.polarity
            if topic[0] not in results[business_id]:
                results[business_id][topic[0]] = {
                    'count': 0,
                    'positive': 0,
                    'negative': 0,
                    'reviews': {}
                }
            results[business_id][topic[0]]['reviews'][review_id[0]] = {'snippet': business_review_data.text, 'polarity': polarity}
            results[business_id][topic[0]]['count'] += 1
            if polarity > 0:
                results[business_id][topic[0]]['positive'] += 1
            else:
                results[business_id][topic[0]]['negative'] += 1

# output csvs locally
#for key, value in results['vcNAWiLM4dR7D2nwwJ7nCA'].iteritems():
for business_id, sentiment_data in results.iteritems():
    header = ['name','word','count','positive', 'negative', 'review_ids']
    temp = []
    for key, value in results[business_id].iteritems():
        review_ids = []
        for review in value['reviews'].iterkeys():
            review_ids.append(review)
        if int(value['count']) != 1:
            temp.append([key, key, value['count'], 100 * value['positive'] / value['count'], 100 * value['negative'] / value['count'], review_ids])
    csv_io.array_to_csv(business_id + '.csv', temp, header)
