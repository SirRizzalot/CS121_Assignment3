############################################################
# load in data
# 1. determining weights
# 2. create scoring functions
# 3. compare scores
############################################################
from sklearn.feature_extraction.text import TfidfVectorizer
from PartA import tokenizeHTMLString
from Retrieval import load_websitetxt, load_datatxt
from collections import defaultdict
import math

keys = ["class","zzxyz"]
# retrieve data from index files
# for now, website_data: 
# {word1:[(tf,sp,id),(tf,sp,id),(tf,sp,id)], word2:[(tf,sp,id),(tf,sp,id)]}
website_data = load_websitetxt('website_index.txt', keys)
url_data = load_datatxt('url_ids.txt')
url_no = len(url_data)

# score and sort the list of urls for each word in the index
class Ranker:
    def __init__(self, word):
        self.word = word
        if (word in website_data):
            self.posting = website_data[word] # list of all postings of the word
        self.tfidf_score = {}
        self.score = {} # {url1:score1, url2:score2,....}
    
    
    # a function to calculate idf for a word
    # receive a posting list of a single word and calculate idf score for that word
    # notice that IDF score is typically shared among all postings of the same word in the inverted index.
    def calculateIDF(self):     
        document_frequency = len(self.posting) # no of document the word appears
        idf_score = math.log(url_no / document_frequency)
            
        return idf_score
        
    # a function to calculate tf for all postings of a word
    # receive a posting list of a single word and calculate tf score for all postings of that word
    def calculateTF(self):
        tf_scores = {}
        for document in self.posting:
            doc_id = document[2]
            term_frequency = document[0]
            tf_scores[doc_id] = 1 + math.log(term_frequency)  # right formular will be 1 + math.log(tf / word_count)
    
        return tf_scores
    
    def calculateTFIDF(self):
        # check if the word is in the index
        if self.word in website_data:
            idf_score = self.calculateIDF()
            tf_scores = self.calculateTF()
            tfidf_scores = {}
            for document in self.posting:
                doc_id = document[2]
                doc_tf = tf_scores[doc_id]
                doc_score = doc_tf * idf_score
                tfidf_scores[doc_id] = doc_score
                
            
            #return tfidf_scores 
            self.tfidf_score = tfidf_scores
        else:
            # if word is not in the index, self.tfidf score of the word will be 0
            self.tfidf_score = 0
            
    # posting is the array of posting for a word
    # needs to call self.calculateTFIDF() to get the dict of tfidf score of all postings of the word
    def getscore(self):
        # check if the word is in the index
        if self.word in website_data:           
            # calculate tfidf scores
            self.calculateTFIDF() 
            for document in self.posting:
                doc_id = document[2]
                #get document tf-idf value
                self.score[doc_id] = self.tfidf_score[doc_id]
                # if the special_frequency is not 0
                if document[1] > 0:
                   self.score[doc_id] = document[1]
            #return self.score
    
    #sort the urls by score
    def sorturl(self):
        sorted_score = sorted(self.score.items(), key= lambda x:x[1], reverse = True)
        self.score.clear()
        for key,value in sorted_score:
            self.score[key] = value
        return self.score

    # WILL BE IMPLEMENTED ******************************
    def get_tf_idf_of_query_words(self, query):
        # search through the website_index dictionary
        # to get specific words in query, get posting list
        # then take the top 5 queries 
        return 0
    
if __name__ == '__main__':
    word_rank = Ranker("class")
    word_rank.getscore()
    print(word_rank.sorturl())