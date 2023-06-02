from collections import defaultdict
import csv


class QueryDB(object):

    def __init__(self):
        self.id_to_index = self.load_datatxt()
        self.url_id_to_string = self.load_urlId()
        self.Queries = list()
        self.words_locations = dict()
        #self.intersect_list = self.intersection_term_docs()
        self.url_no = len(self.url_id_to_string)
        
    #open text file and sets term as key and line number as value
    def load_datatxt(self):
        data = {}
        with open('word_index_locator.txt') as file:
            for line in file:
                line = line.strip()
                key, value = line.split(' : ')
                data[key] = value
                
        return data

    #given a word list (based on query) gets term and line number
    #filters larger dictionary into smaller dictionary based on query then gives line numbers
    def get_location(self, word_list):
        data = {}
        for k in word_list:
            try:
                data[k] = int(self.id_to_index[k])
            except KeyError:
                data[k] = 0
        
        return data.items()

    #gets urID and url as a dictionary
    def load_urlId(self):
        data = {}
        with open('url_ids.txt') as file:
            for line in file:
                line = line.strip()

                key, value = line[1:-1].split(': ')
                data[int(key)] = value
        return data

    #term and postings
    def load_websitetxt(self, list_of_location):
        data = defaultdict(list)
        #print(type(list_of_location), list_of_location)
        # keys = text.split()
        with open('website_index.txt') as file:
            counter = 1
            for word,location in list_of_location:
                
                if int(location) == 0:
                    continue
                while counter < int(location):
                    file.readline()
                    counter += 1
                line = file.readline()
                counter += 1
                line = line.strip()
                key, value = line.split(': ')
                value1 = value[1:-1].replace("'", "").split(", ")
                for i in value1:
                    info = i.split(",")
                    int_info = [int(x) for x in info]
                    data[key].append(int_info)
        # print(data)
        return data
    #gets urls 
    
    def intersection_term_docs(self, word_list):
            '''get union of all documents in query list'''
            intersection_doc = []
            doc_list = []
            #print("ID ", list(self.id_to_index["query"]))
            invert_index = self.load_websitetxt(self.get_location(word_list))
            #print(self.word_list)
            for posting in invert_index.values():
                temp_doc = set([doc[0] for doc in posting])
                
                doc_list.append(temp_doc)
            
            print("or" not in word_list)
            if len(doc_list) != 0 and "or" not in word_list:
                #https://stackoverflow.com/questions/3852780/python-intersection-of-multiple-lists
                intersection_doc = set(doc_list[0]).intersection(*doc_list)
            else:
                union_list = []
                or_pos = word_list.index("or")
                if or_pos != 0 and or_pos != len(word_list):
                
                    union_list =  doc_list[or_pos-1] + doc_list[or_pos+1]
                    doc_list.remove(doc_list[or_pos])
                    doc_list.remove(doc_list[or_pos-1])
                    doc_list.remove(doc_list[or_pos+1])
                    intersection_doc = set(union_list).intersection(*doc_list)
            return intersection_doc
    

        

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


