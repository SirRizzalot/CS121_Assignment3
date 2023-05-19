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
from numpy import dot
from numpy.linalg import norm

keys = ["clase","clasp"]
# retrieve data from index files
# for now, website_data: 
# {word1:[(tf,sp,id),(tf,sp,id),(tf,sp,id)], word2:[(tf,sp,id),(tf,sp,id)]}
website_data = load_websitetxt('website_index.txt', keys)
url_data = load_datatxt('url_ids.txt')
url_no = len(url_data)
#print(url_data)

# score and sort the list of urls for each word in the index
class Ranker:
    def __init__(self, word, database):
        self.database = database
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
                # if the special_frequency is not 0 (means the word appears at special case in the doc)
                # add extra weight to the score 
                if document[1] > 0:
                   self.score[doc_id] += document[1]

    
    #sort the urls by score
    def sorturl(self):
        sorted_score = sorted(self.score.items(), key= lambda x:x[1], reverse = True)
        self.score.clear()
        for key,value in sorted_score:
            self.score[key] = value
        return self.score

# calculate tf_idf score list for the query
def get_tf_idf_of_query_words(queryWordList):
    query_score = []   # format: [word1_score, word2_score, word3_score]
    for word in queryWordList:
        if word not in website_data:
            query_score.append(0)
        else:
            # calculate tf
            word_frequency = queryWordList.count(word)
            tf_score = 1 + math.log(word_frequency / len(queryWordList))
            
            # calculate idf
            document_frequency = len(website_data[word]) # no of document the word appears
            idf_score = math.log(url_no / document_frequency)

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

   
if __name__ == '__main__':
    query_words = ["clase","clasp"]
    score_list = {}
    # loop through all words in the query to get score set of all postings having that word
    # score_list has the form:
    # {
    #     word: {doc:score, doc:score, doc:score},
    #     word: {doc:score, doc:score}
    # }
    for word in query_words:
        word_rank = Ranker(word, "database")
        word_rank.getscore()
        score_list[word] = word_rank.score

    # get query tfidf score
    query_score = get_tf_idf_of_query_words(query_words)
    
    #dictionary format of score of words in query for all urls having them
    # {
    #     url1: {score_w1, score_w2, score_w3},
    #     url2: {score_w1, score_w2, score_w3},
    #     url3: {score_w1, score_w2, score_w3},
    # }
    all_doc_vector = {}
    for word in query_words:
        for url in url_data:
            url = int(url[1:])
            if url in score_list[word]:
                if url in all_doc_vector:
                    all_doc_vector[url].append(score_list[word][url])
                else:
                    all_doc_vector[url] = []
                    all_doc_vector[url].append(score_list[word][url])
                #doc_score = get_tf_idf_of_a_doc(query_words, score_list, url)
                #cos_sim = compute_cosine_similarities(query_score, doc_score)
                #print(cos_sim)

    # add score 0 to words not appear in url but appears in query
    for url in all_doc_vector:
        if len(all_doc_vector[url]) < len(query_words):
            for i in range(len(query_words) - len(all_doc_vector[url])):
                all_doc_vector[url].append(0)
        
    
    for doc in all_doc_vector:
        cos_sim = compute_cosine_similarities(query_score, all_doc_vector[doc])
        print(f"{doc} : {cos_sim}")
    