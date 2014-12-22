from mrjob.job import MRJob
import sys
import re

WORD_RE = re.compile(r"[^\[\]][a-zA-Z]+")

class Inverted(MRJob):

    def mapper(self, _, review):
        words = review.split()
        biz = words[0].strip('"')
        word_list = list()
        for w in words[1:]:
            word = WORD_RE.search(w)
            if word:
                word = word.group(0).strip('"')
                yield word, biz

    def reducer(self, key, value):
        yield key, list(value)

if __name__ == '__main__':
    Inverted.run()
