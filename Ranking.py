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

# class Ranker:
#     def __init__(self):
#         self.no_of_document = 1988
#         self.tfidf_dict = defaultdict(list)
        
#     def compute_tf_idf_weight_old(doc):
#         vectorizer = TfidfVectorizer(tokenizer=tokenizeHTMLString) # in PartA.py
        
#         # Compute the TF-IDF scores for the given document
#         tfidf_matrix = vectorizer.fit_transform([doc])
        
#         # Get the feature names (words)
#         feature_names = vectorizer.get_feature_names_out()
        
#         # Get the TF-IDF scores for the document
#         tfidf_scores = tfidf_matrix.toarray()[0]
        
#         # Create a dictionary to store the word and its corresponding TF-IDF score
#         tfidf_dict = {}
#         for word, score in zip(feature_names, tfidf_scores):
#             tfidf_dict[word] = score
        
#         return tfidf_dict

#     def compute_tf_idf_weight(self, doc, frequencies):
#         total_words = len(doc.split())
#         for word,count in frequencies.items():
#             tf = 1 + math.log(count / total_words)
#             idf = math.log(self.no_of_documents / self.get_document_frequency(word))
#             self.tfidf_dict[word] = tf * idf
#         return self.tfidf_dict
       
#     def get_document_frequency(self,word):
#         return len(word_url[word])
    
    
def compute_tf_idf_weight(doc):
        vectorizer = TfidfVectorizer(tokenizer=tokenizeHTMLString) # in PartA.py
        
        # Compute the TF-IDF scores for the given document
        tfidf_matrix = vectorizer.fit_transform([doc])
        
        # Get the feature names (words)
        feature_names = vectorizer.get_feature_names_out()
        
        # Get the TF-IDF scores for the document
        tfidf_scores = tfidf_matrix.toarray()[0]
        
        # Create a dictionary to store the word and its corresponding TF-IDF score
        tfidf_dict = {}
        for word, score in zip(feature_names, tfidf_scores):
            tfidf_dict[word] = score
        
        return tfidf_dict