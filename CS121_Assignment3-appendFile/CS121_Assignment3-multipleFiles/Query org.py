############################################################
# load in data
# 1. determine what to find -> dictionary(word:urls)
# booleanQuery ands and ors
############################################################
import ast
import csv
import os
import json
from collections import defaultdict

from PartA import tokenizeHTMLString, computeWordFrequencies
import string
from sys import argv
import time
from bs4 import BeautifulSoup
import lxml
#map = 'key' = word 'value' = document, frequency
#k = number of documents

#skip lists index the index

#conjunctive processing
#one assumption every return document must have all terms
invert_index = defaultdict()
query_index = defaultdict()
def test_dict():
     
    word_index = open("website_index.txt", encoding='utf-8')
    for line in word_index:
        
        temp_line = line.split(':',1)
        temp_value = temp_line[1].replace('\n', '')
        temp_value = temp_line[1].strip()
        #print(temp_value)
        temp_value_list = ast.literal_eval(temp_value)
        #print(temp_line[0])
        word_key = temp_line[0]
        invert_index[word_key] = temp_value_list
    #print(invert_index) 
    word_index.close()



def conjunctive_processing(query, word_index_locator):
    #query_doc_list = 
    query_list = query.split()
    temp_doc_list = []
    for word in query_list:
        if word in invert_index:
            temp_list = []
            for value in invert_index[word]:
                doc_id = value[0]
                temp_list.append(doc_id)
        else:
            continue
        temp_doc_list.append(temp_list)

    if len(temp_doc_list) >= len(query_list):
        query_doc = temp_doc_list[0]
        for i in range(len(query_list)-1):
            query_inter = set(query_doc).intersection(set(temp_doc_list[i+1]))
            query_doc = query_inter
        return(list(query_doc))
    else:
        return list()

#def document_Time_retrieval(Query,Index,feature_fuction_f,feature_function_g,k):
    #retrieve all posting lists

    #loop over all documents
    #for each document go over posting list and update document score
    #for all query terms
    #add score to ranking
    #sort ranking queue top k results
    #return






def generate_ngrams(sentence):
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

if __name__ == "__main__":
    test_dict()
    query = "school senior lectur lender"
    print(conjunctive_processing(query, invert_index))
    