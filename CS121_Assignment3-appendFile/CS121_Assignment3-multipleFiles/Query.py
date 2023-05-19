############################################################
# load in data
# 1. determine what to find -> dictionary(word:urls)
# booleanQuery ands and ors
############################################################

#All you need to do is break the query up, 
# find the location of each word. 
# Sort the word into increasing order by their location and call Anthony’s function
from Retrieval import load_data
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
#query_ws_locator = defaultid(list)
def query(query_search_terms):
    query_list = query_search.strip().split()
    return query_list

query_invert_index = defaultdict(list)
#goes and creates a smaller inverted index 
def get_query_website(query_search):
     
    data = load_data("website_index.csv")
    query_list = query_search.strip().split()
    
    for word in query_list:
        #print(word)
        #gets value which is list of documents and frequencies
        
        word_index = data[word]
        
        query_invert_index[word] = word_index





if __name__ == "__main__":
    query = "school senior lectur lender"
    print(get_query_website(query))