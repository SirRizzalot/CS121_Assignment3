############################################################
# load in data
# need to load in url_ids.txt -> dictionary
# need to load in word_index_locator.txt  -> dictionary
# given a specific line or lines, load in from website_index.csv
# needs to fast
# don't load in too much -> list of urls
############################################################

import csv
import os
import json
from collections import defaultdict
import string
from sys import argv
import time
from collections import defaultdict
import csv
import ast

def load_datatxt(file_name):
    data = {}
    with open(file_name) as file:
        for line in file:
            line = line.strip()
            key, value = line.split(': ') or line.split(',')
            data[key] = value
    return data


def load_websitetxt(filename, keys):
    data = {}
    with open(filename) as file:
        for line in file:
            line = line.strip()
            key, value = line.split(': ')

            if key in keys:
                value1 = value[1:-1].replace("'","").split(", ")

                data[key] = [tuple(map(int, i.split(','))) for i in value1]
    return data 



if __name__ == '__main__':
    # url_data = load_datatxt('url_ids.txt')
    # print(url_data)

    # word_data = load_datatxt('word_index_locator.txt')
    # print(word_data)

    keys = ["class"]
    website_data = load_websitetxt('website_index.txt', keys)
    print(website_data)