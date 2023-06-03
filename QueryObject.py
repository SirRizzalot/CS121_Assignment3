from collections import defaultdict
import csv
import ast
from itertools import islice
import time
import pandas as pd
import linecache


csv.field_size_limit(2**31-1)

class QueryDB(object):

    def __init__(self):
        # self.id_to_index = self.load_datatxt()
        self.id_to_index = self.load_index_bytescsv()
        self.url_id_to_string = self.load_urlId()
        self.Queries = list()
        self.words_locations = dict()
        self.url_no = len(self.url_id_to_string)

    # function to load information from word_index_locator.txt file
    # def load_datatxt(self):
    #     data = {}
    #     with open('word_index_locator.txt') as file:
    #         for line in file:
    #             line = line.strip()
    #             key, value = line.split(' : ')
    #             data[key] = value
    #     return data
    
    # function to load information from word_index_locator.csv file
    # def load_datatxt(self):
    #     data = {}
    #     with open('word_index_locator.csv', newline='') as file:
    #         reader = csv.reader(file)
    #         for row in reader:
    #             key, value = row[0], row[1]
    #             data[key] = value
    #     return data
    
    def load_index_bytescsv(self):
        data = {}
        with open('tfidf_index_locator.csv', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                key, value = row[0], row[1]
                data[key] = value
        return data

    
    def get_location(self, word_list):
        data = {}
        for k in word_list:
            try:
                data[k] = int(self.id_to_index[k])
            except KeyError:
                data[k] = 0
        #print(data.items())
        return data.items()

    # function to load information from url_ids.txt file
    # def load_urlId(self):
    #     data = {}
    #     with open('url_ids.txt') as file:
    #         for line in file:
    #             line = line.strip()

    #             key, value = line[1:-1].split(': ')
    #             data[int(key)] = value
    #     return data

    # function to load information from url_ids.csv file
    def load_urlId(self):
        data = {}
        with open('url_ids.csv', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                key, value = row[0], row[1]
                data[int(key)] = value
        return data
    
    # def seek_position(self, position):


    # function to load information from website_index.txt file
    # def load_websitetxt(self, list_of_location):
    #     data = defaultdict(list)
    #     start = time.time()
    #     # keys = text.split()
    #     print("list_of_locaiton", list_of_location)
    #     with open('website_index.txt') as file:
    #         counter = 1

    #         for word, location in list_of_location:
    #             if location == 0:
    #                 continue

    #             loc = 18829411
    #             file.seek(loc)
    #             # while counter < location:
    #             #     file.readline()
    #             #     counter += 1
    #             line = file.readline()
    #             print("line", line)
    #             break
    #             counter += 1
    #             line = line.strip()
    #             key, value = line.split(': ')
    #             value1 = value[1:-1].replace("'", "").split(", ")
    #             for i in value1:
    #                 info = i.split(",")
    #                 # print(counter, info)
    #                 # for x in info:
    #                     # print(x, type(x))
                    
    #                 int_info = [int(x) for x in info]
    #                 data[key].append(int_info)
    #     # print(data)
    #     end = time.time()
    #     print("total time for here", end-start)
    #     return data


   

    # function to load information from website_index.csv file
    # def load_websitetxt(self, list_of_location):
    #     data = defaultdict(list)
    #     print("list", list_of_location)
    #     start = time.time()

    #     with open('website_index.csv', newline='') as file:
    #         reader = csv.reader(file)
    #         for word, location in list_of_location:
    #             if location == 0:
    #                 continue

    #             # Move to the desired line using islice
    #             reader = islice(reader, location - 1, None)

    #             temp = time.time()
    #             print("iSlice time", temp-start)

    #             try:
    #                 row = next(reader)
    #                 key, value = row[0], row[1]
    #                 data[key].append(value)
    #                 break
    #                 value1 = value[1:-1].replace("'", "").split("}, ")

    #                 for i in value1:
    #                     info = i.split(',{')
    #                     temp = info[0].split(",")
    #                     temp.append(set(info[1:]))

    #                     if temp[4] == 'set()':
    #                         while len(temp) > 0:
    #                             temp[0] = temp[0].lstrip()
    #                             data[key].append(tuple(temp[:5]))
    #                             temp = temp[5:]
    #                     else:
    #                         data[key].append(tuple(temp))
    #             except StopIteration:
    #                 # Handle the case when there are no more lines to read
    #                 break
    #     # print(data)
    #     end = time.time()
    #     print("parsing time", end-start)
    #     return data

    def load_tfidf_index(self, list_of_location):
        data = defaultdict(list)
        start = time.time()

        with open('tfidf_index.csv', newline='') as file: 
            for word, location in list_of_location:
                if location == 0:
                    continue
                file.seek(location)
                row = file.readline()
                # print("row", row)

                value1 = row[len(word)+3:-4].replace("'", "").split("), ")
                the_word = row[:len(word)]
                # print("value1", value1)
                
                
                for i in value1:
                    info = i.split(', ')
                    # print("info", info)
                    
                    word = info[0]
                    word = word[1:]
                    temp = []
                    temp.append(int(word))
                    temp.append(float(info[1]))
                    if info[2].endswith(")"):
                        word = info[1]
                        word = word[:-1]
                        temp.append(float(word))
                    else:
                        temp.append(float(info[2]))
                    # print("temp", temp)
                    data[the_word].append(tuple(temp))
        end = time.time()
        print("parsing time", end-start)
        print("data", data)
        return data

    

    def load_websitetxt(self, list_of_location):
        data = defaultdict(list)
        start = time.time()

        with open('website_index.csv', newline='') as file: 
            for word, location in list_of_location:
                if location == 0:
                    continue
                file.seek(location)
                row = file.readline()

                value1 = row[len(word)+3:-3].replace("'", "").split("}, ")
                
                for i in value1:
                    info = i.split(',{')
                    temp = info[0].split(",")
                    temp.append(set(info[1:]))
                    if temp[4] == 'set()':
                        while len(temp) > 0:
                            temp[0] = temp[0].lstrip()
                            data[word].append(tuple(temp[:5]))    
                            temp = temp[5:]
                    else:
                        data[word].append(tuple(temp))
        end = time.time()
        print("parsing time", end-start)
        return data

    def get_urls(self, data):
        url_nums = []
        for _, value in data.items():
            for elements in value:
                # print(elements[2])
                url_nums.append(int(elements[2]))
        url_nums.sort()

        # print(url_nums)

        urls = []
        url_data = self.load_urlId('url_ids.txt')
        # print(url_data)
        for num in url_nums:
            urls.append(url_data[num])

        return urls