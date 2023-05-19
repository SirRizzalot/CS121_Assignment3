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

from collections import defaultdict
import csv
def load_datatxt(file_name):
    data = {}
    with open(file_name) as file:
        for line in file:
            line = line.strip()
            key, value = line.split(' : ')
            data[key] = value
    return data

def load_urlId(file_name):
    data = {}
    with open(file_name) as file:
        for line in file:
            line = line.strip()
            
            key, value = line[1:-1].split(': ')
            data[int(key)] = value
    return data

def load_websitetxt(filename, text):
    data = defaultdict(list)
    keys = text.split()
    with open(filename) as file:
        for line in file:
            line = line.strip()
            key, value = line.split(': ')

            if key in keys:
                value1 = value[1:-1].replace("'","").split(", ")

                for i in value1:
                    data[key].append(i.split(","))
    return data 

def get_urls(data):
    url_nums = []
    for _, value in data.items():
        for elements in value:
            # print(elements[2])
            url_nums.append(int(elements[2]))
    url_nums.sort()

    # print(url_nums)

    urls = []
    url_data = load_urlId('url_ids.txt')
    # print(url_data)
    for num in url_nums:
        urls.append(url_data[num])


    return urls





if __name__ == '__main__':
    # url_data = load_urlId('url_ids.txt')
    # print(url_data)

    # word_data = load_datatxt('word_index_locator.txt')
    # print(word_data)

    text = "zyl zzxyz"
    website_data = load_websitetxt('website_index.txt', text)
    print(website_data)

    # urls = get_urls(website_data)
    # print(urls)

    


