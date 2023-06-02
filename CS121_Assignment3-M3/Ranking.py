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
from numpy import dot
from numpy.linalg import norm

# # retrieve data from index files
# # for now, website_data: 
# # {word1:[(tf,sp,id),(tf,sp,id),(tf,sp,id)], word2:[(tf,sp,id),(tf,sp,id)]}
# website_data = load_websitetxt('website_index.txt', keys)
# url_data = load_datatxt('url_ids.txt')
# url_no = len(url_data)
# #print(url_data)

# score and sort the list of urls for each word in the index
class Ranker:
    def __init__(self, word, query_list, data):
        self.data = data
        self.query_list = query_list
        self.word_info = self.data.word_info
        self.url_no = self.data.parent.url_no
        self.word = word
        if (word in self.word_info):
            self.posting = self.word_info[word] # list of all postings of the word
        self.tfidf_score = {}
        self.score = {} # {url1:score1, url2:score2,....}
    
    # a function to calculate idf for a word
    # receive a posting list of a single word and calculate idf score for that word
    # notice that IDF score is typically shared among all postings of the same word in the inverted index.
    def calculateIDF(self):     
        document_frequency = len(self.posting) # no of document the word appears
        idf_score = math.log(self.url_no / document_frequency)
        return idf_score
        
    # a function to calculate tf for all postings of a word
    # receive a posting list of a single word and calculate tf score for all postings of that word
    def calculateTF(self):
        tf_scores = {}
        for document in self.posting:
            doc_id = document[0]
            term_frequency = document[0]
            tf_scores[doc_id] = 1 + math.log(term_frequency)  # right formular will be 1 + math.log(tf / word_count)
    
        return tf_scores
    
    def calculateTFIDF(self):
        # check if the word is in the index
        if self.word in self.word_info:
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
        intersection_list = self.data.parent.intersection_term_docs(self.query_list)
        # check if the word is in the index
        if self.word in self.word_info:          
            # calculate tfidf scores
            self.calculateTFIDF() 
            if len(intersection_list) !=0:
                
                for document in self.posting and document in intersection_list:
                    doc_id = document[0]
                    #get document tf-idf value
                    self.score[doc_id] = self.tfidf_score[doc_id]
                    # if the special_frequency is not 0 (means the word appears at special case in the doc)
                    # add extra weight to the score 
                    if document[1] > 0:
                        self.score[doc_id] += document[1]
            else:
                for document in self.posting:
                    doc_id = document[0]
                    #get document tf-idf value
                    self.score[doc_id] = self.tfidf_score[doc_id]
                    # if the special_frequency is not 0 (means the word appears at special case in the doc)
                    # add extra weight to the score 
                    if document[1] > 0:
                        self.score[doc_id] += document[1]

    
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
            tf_score = 1 + math.log(word_frequency / len(queryWordList))
            
            # calculate idf
            document_frequency = len(data.word_info[word]) # no of document the word appears
            idf_score = math.log(data.parent.url_no / document_frequency)    # data.parent.url_no (look at url_no of QueryObject class)

            # calculate tf idf
            tfidf_score = tf_score * idf_score
            
            # add current word score the query_score list
            query_score.append(tfidf_score)
    return query_score
 
#after having score_list
# receive a list of query words and score_list of ALL DOCS for ALL WORDS IN THE QUERY
# make a list for score of ONE DOC containing ALL WORDS IN THE QUERY  
# def get_tf_idf_of_a_doc(query_words, score_list, doc_id):
#     doc_score = set() # format: doc = (score_w1, score_w2, score_w3)
#     for word in query_words:
#         if word not in score_list:
#             doc_score.add(0)
#         else:
#             word_score = score_list[word][doc_id]
#             print(word_score)
#             doc_score.add(word_score)
#     return doc_score
            
#compute cosine similarities
def compute_cosine_similarities(query_score, document_score):
    cos_sim = dot(query_score, document_score)/(norm(query_score)*norm(document_score))
    return cos_sim

   