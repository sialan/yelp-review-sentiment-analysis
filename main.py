import argparse
import sys


def run_local_key():
	pass

def run_remote():
	pass

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding("utf-8")

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--type', required=True, choices=['keyphrase', 'topic'])
	args = parser.parse_args()

	model_type = args.type
	
	# sample csv
	if model_type == 'keyphrase':
		print(model_type)
	elif model_type == 'topic':
		print(model_type)
