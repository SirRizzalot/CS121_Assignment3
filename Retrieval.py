############################################################
# load in data
# 1. need to load in url_ids.txt -> dictionary
# 2. need to load in word_index_locator.txt  -> dictionary
# 3. given a specific line or lines, load in from website_index.csv
#    + needs to fast
#    + don't load in too much -> list of urls
############################################################

# import csv
# import os
# import json
# from collections import defaultdict
# import string
# from sys import argv
# import time

import csv

def load_data(file_name, separator):
    data = {}
    with open(file_name, newline='') as file:
        reader = csv.reader(file, delimiter=separator)
        for row in reader:
            key = row[0]
            value = row[1:]
            data[key] = value
    return data

def load_website(keys):
    data = []
    with open('website_index.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            key = row[0]
            if key in keys:
                data.append(row[1])
    return data
                





if __name__ == '__main__':
    # url_data = load_data('url_ids.csv', ',')
    # word_data = load_data('word_index_locator.csv', ',')
    # website_data =load_data('website_index.csv', ',')
    keys = ["two", "which", "uci"]
    website_data = load_website(keys)
    # print("URL Data:")
    # print(url_data)
    # print("\nWord Data:")
    # print(word_data)
    print("Website Data:")
    print(website_data)


