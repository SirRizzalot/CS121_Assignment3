############################################################
# load in data
# 1. determining weights
# 2. create scoring functions
# 3. compare scores
############################################################
from sklearn.feature_extraction.text import TfidfVectorizer
from PartA import tokenizeHTMLString
from collections import defaultdict
import math
import numpy
from numpy import dot
from numpy.linalg import norm
from scipy.special import logsumexp

# # retrieve data from index files
# # for now, website_data: 
# # {word1:[(tf,sp,id),(tf,sp,id),(tf,sp,id)], word2:[(tf,sp,id),(tf,sp,id)]}
# website_data = load_websitetxt('website_index.txt', keys)
# url_data = load_datatxt('url_ids.txt')
# url_no = len(url_data)
# #print(url_data)

# score and sort the list of urls for each word in the index
class Ranker:
    def __init__(self, word, data):
        self.data = data
        self.word_info = self.data.word_info
        self.url_no = int(self.data.parent.url_no)
        self.word = word
        if (word in self.word_info):
            self.posting = self.word_info[word] # list of all postings of the word
        self.tfidf_score = {}
        self.score = {} # {url1:score1, url2:score2,....}
        self.special_score = {} # {url1:specialscore1, url2:specialscore2,...} - special score is 0 if the word is not of special case
    
            
    # # a function to calculate idf for a word
    # # receive a posting list of a single word and calculate idf score for that word
    # # notice that IDF score is typically shared among all postings of the same word in the inverted index.
    # def calculateIDF(self):     
    #     document_frequency = len(self.posting) # no of document the word appears
    #     idf_score = math.log10(self.url_no / document_frequency)
    #     return idf_score
        
    # # a function to calculate tf for all postings of a word
    # # receive a posting list of a single word and calculate tf score for all postings of that word
    # def calculateTF(self):
    #     tf_scores = {}
    #     for document in self.posting:
    #         doc_id = int(document[0])
    #         term_frequency = int(document[1])
    #         word_count = int(document[3])
    #         # check if values are valid for doing log
    #         if term_frequency != 0 and word_count != 0:
    #             tf_scores[doc_id] = 1 + math.log10(term_frequency / word_count)  # right formular will be 1 + math.log(tf / word_count)
    #         else:
    #             tf_scores[doc_id] = 0
    #     return tf_scores
    
    # def calculateTFIDF(self):
    #     # check if the word is in the index
    #     if self.word in self.word_info:
    #         idf_score = self.calculateIDF()
    #         tf_scores = self.calculateTF()
    #         tfidf_scores = {}
    #         for document in self.posting:
    #             doc_id = int(document[0])
    #             doc_tf = tf_scores[doc_id]
    #             doc_score = doc_tf * idf_score
    #             tfidf_scores[doc_id] = -doc_score
    #         #return tfidf_scores 
    #         self.tfidf_score = tfidf_scores
    #     else:
    #         # if word is not in the index, self.tfidf score of the word will be 0
    #         self.tfidf_score = 0
    def getScore(self):
        if self.word in self.word_info:
            for document in self.posting:
                doc_id = int(document[0])  
                # get tfidf score    
                score = float(document[1])
                self.tfidf_score[doc_id] = score
                # get special case score
                special_freq = int(document[2])   
                if special_freq > 0:
                    self.special_score[doc_id] = math.log10(special_freq)  
                else:
                    self.special_score[doc_id] = 0
            
    # def getscore(self):
    #     # check if the word is in the index
    #     if self.word in self.word_info:
    #         #get TFIDF scores            
    #         self.getTFIDF() 
    #         print(self.tfidf_score) 
    #         for document in self.posting:
    #             doc_id = int(document[0])    
    #             # get document tf-idf value
    #             self.score[doc_id] = self.tfidf_score[doc_id]
        
    # # posting is the array of posting for a word
    # # needs to call self.calculateTFIDF() to get the dict of tfidf score of all postings of the word
    # def getscore(self):
    #     # check if the word is in the index
    #     if self.word in self.word_info:          
    #         # calculate tfidf scores
    #         self.calculateTFIDF() 
    #         for document in self.posting:
    #             doc_id = int(document[0])
    #             #get document tf-idf value
    #             self.score[doc_id] = self.tfidf_score[doc_id]
    #             # if the special_frequency is not 0 (means the word appears at special case in the doc)
    #             # add extra weight to the score 
    #             # if int(document[2]) > 0:
    #             #    self.score[doc_id] += int(document[2])

    # def get_special_score(self):
    #     if self.word in self.word_info:
    #         for document in self.posting:
    #             doc_id = int(document[0])
    #             if int(document[2]) > 0:
    #                 special_score = math.log10(int(document[2]))
    #             else:
    #                 special_score = 0
    #             self.special_score[doc_id] = special_score
     
#sort the urls by score
def sorturl(dict):
    sorted_score = sorted(dict.items(), key= lambda x:x[1], reverse = True)
    dict.clear()
    for key,value in sorted_score:
        dict[key] = value
    return dict

# calculate tf_idf score list for the query
def get_tf_idf_of_query_words(queryWordList, data):
    query_score = []   # format: [word1_score, word2_score, word3_score]
    for word in queryWordList:
        if word not in data.word_info:  # data.word_info (look at word_info of Query class)
            query_score.append(0)
        else:
            # calculate tf
            word_frequency = queryWordList.count(word)
            tf_score = 1 + math.log10(word_frequency / len(queryWordList))
            
            # calculate idf
            document_frequency = len(data.word_info[word]) # no of document the word appears
            idf_score = math.log10(int(data.parent.url_no) / document_frequency)    # data.parent.url_no (look at url_no of QueryObject class)

            # calculate tf idf
            tfidf_score = tf_score * idf_score
            
            # add current word score the query_score list
            query_score.append(tfidf_score)
    return query_score

#compute cosine similarities
def compute_cosine_similarities(query_score, document_score):
    if numpy.count_nonzero(query_score) == 0 or numpy.count_nonzero(document_score) == 0:
        return 0.0
    else:
        cos_sim = dot(query_score, document_score)/(norm(query_score)*norm(document_score))
        return cos_sim

   
