############################################################
# load in data
# 1. determine what to find -> dictionary(word:urls)
# booleanQuery ands and ors
############################################################
from collections import defaultdict
from nltk.stem import PorterStemmer
import time


class Query(object):
    
    def __init__(self, parent):
        self.parent = parent
        self.query = list()
        # query words
        self.word_info = defaultdict()
        # word : url data
        self.no_show = set()
        # set of words that does not have an url

    def querying(self):
        stem = PorterStemmer()
        find = True
        #while find:

        self.query = input("what do you want to search? enter quit to quit\n").lower().split()
        # if " ".join(self.query) == "quit":
        #     find = False
        #     break
        self.query = [stem.stem(i) for i in self.query]
        ordered = sorted(self.parent.get_location(self.query), key=lambda x: x[1])
        #print(ordered)

        self.no_show = {i for i in ordered if i[1] == 0}
        #print(self.no_show)
        
        start = time.time()
        # self.word_info = self.parent.load_websitetxt(ordered)
        self.word_info = self.parent.load_tfidf_index(ordered)
        end = time.time()
        print("loading word_site.csv", end - start)
        #print(self.word_info)
        #print(self.word_info.items())
        # score_list = {}
        # for word in self.query:
        #     word_rank = Ranker(word, self)
        #     word_rank.getScore()
        #     score_list[word] = word_rank.score


    def generate_ngrams(self,sentence):
        words = sentence.split()
        n = len(words)
        ngram_map = {}

        for i in range(n, 0, -1):
            ngrams = []
            for j in range(0, n - i + 1):
                ngram = ' '.join(words[j:j + i])
                ngrams.append(ngram)

            ngram_map[i] = ngrams

        return ngram_map