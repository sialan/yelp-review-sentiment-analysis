import pandas as pd
from textblob import TextBlob
import argparse
import sys

from src.util import csv_io, reservoir_sampling
from src import features


def run_local_sentiment_by_keyphrase(sample_business_data, sample_review_data):
    results = {}

    for business_id, business_row_data in sample_business_data.iterrows():
        results[business_id] = {}
        
        # Iterate through all reviews for associated business_id
        for review_id, business_review_data in sample_review_data[sample_review_data.index.get_level_values(1) == business_id].iterrows():
            # Prep and preprocess text
            b = TextBlob(business_review_data.text)
            cleaned = " ".join([x for x in b.words])

            # Extract top keywords for current review
            keyphrases = features.extract_top_keywords(cleaned)

            # Loop through each sentence and predict polarity
            polarity = b.sentiment.polarity

            for keyphrase in keyphrases:
                if keyphrase[0] not in results[business_id]:
                    results[business_id][keyphrase[0]] = {
                        'count': 0,
                        'mentions': 0,
                        'positive': 0,
                        'negative': 0,
                        'reviews': {}
                    }
                results[business_id][keyphrase[0]]['reviews'][review_id[0]] = {'polarity': polarity, 'review': 'hello', 'snippet': [business_review_data.text]}
                results[business_id][keyphrase[0]]['count'] += 1
                if polarity > 0:
                    results[business_id][keyphrase[0]]['positive'] += 1
                else:
                    results[business_id][keyphrase[0]]['negative'] += 1
    
    return results
    
def run_local_sentiment_by_topic(sample_business_data, sample_review_data):
    pass

if __name__ == '__main__':
    results = {}

    # Local hack to reconfigure system for string processing
    reload(sys)
    sys.setdefaultencoding("utf-8")

    # Parse input arguments
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--type', required=True, choices=['keyphrase', 'topic'])
    args = parser.parse_args()

    # Load local copies of yelp academic dataset for processing
    business_data = pd.read_csv('./data/input/yelp_academic_dataset_business.csv', index_col = 'business_id')
    review_data = pd.read_csv('./data/input/yelp_academic_dataset_review.csv', index_col = ('review_id', 'business_id'))

    # Sample review dataset
    sample_business_ids = reservoir_sampling.generate_sample(100, business_data.index)
    sample_business_data = business_data[business_data.index.isin(sample_business_ids)]
    sample_review_data = review_data[review_data.index.get_level_values(1).isin(sample_business_data.index)]


    if args.type == 'keyphrase':
        results = run_local_sentiment_by_keyphrase(sample_business_data, sample_review_data)
                
    elif args.type == 'topic':
        results = run_local_sentiment_by_topic(sample_business_data, sample_review_data):

    # Write results locally to data/output/ folder
    for business_id, sentiment_data in results.iteritems():
        header = ['name','word','count','positive', 'negative', 'review_ids']
        output = csv_io.reviews_dict_to_array(sentiment_data)
        csv_io.array_to_csv('data/output/'+ business_id + '.csv', output, header)
