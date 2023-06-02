from collections import defaultdict
import csv
import ast

csv.field_size_limit(2**31-1)

class QueryDB(object):

    def __init__(self):
        self.id_to_index = self.load_datatxt()
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
    def load_datatxt(self):
        data = {}
        with open('word_index_locator.csv', newline='') as file:
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

    # function to load information from website_index.txt file
    # def load_websitetxt(self, list_of_location):
    #     data = defaultdict(list)
    #     # keys = text.split()
    #     with open('website_index.txt') as file:
    #         counter = 1
    #         for word, location in list_of_location:
    #             if location == 0:
    #                 continue
    #             while counter < location:
    #                 file.readline()
    #                 counter += 1
    #             line = file.readline()
    #             counter += 1
    #             line = line.strip()
    #             key, value = line.split(': ')
    #             value1 = value[1:-1].replace("'", "").split(", ")
    #             for i in value1:
    #                 info = i.split(",")
    #                 print(counter, info)
    #                 for x in info:
    #                     print(x, type(x))
                    
    #                 int_info = [int(x) for x in info]
    #                 data[key].append(int_info)
    #     # print(data)
    #     return data

    # function to load information from website_index.csv file
    def load_websitetxt(self, list_of_location):
        data = defaultdict(list)
        # data = defaultdict(set)
        # data = defaultdict(tuple)

        # temp_set = set()
        # temp_set.add(32)
        # temp_set.add(50)
        # temp_set.add(87)
        # print(temp_set)
        # return data

        with open('website_index.csv', newline='') as file:
            reader = csv.reader(file)
            counter = 1
            for word, location in list_of_location:
                if location == 0:
                    continue
                while counter < location:
                    next(reader)
                    counter += 1
                row = next(reader)
                counter += 1
                key, value = row[0], row[1]
                # value2 = value.strip('[]"')
                # value3 = value2.split(", ")
                

                # print("value", value, type(value))
                # for i in value2:
                #     print(i)
                # return data


                # Convert the list of elements into a set of tuples

                

                value1 = value[1:-1].replace("'", "").split("}, ")
                # print("value1", value1)
                for i in value1:
                    
                    # print("tuple(i)", tuple(i), type(tuple(i)))
                    info = i.split(',{')
                    # print(counter, info)
                    # for x in info:
                    #     print(x, type(x))

                    # int_info = [int(x) for x in info]
                    # print("info", info, type(info))
                    
                    # print("tuple_temp", tuple_temp)
                
                    # for x in info:
                    #     print("x", x)

                    
                    temp = info[0].split(",")
                    temp.append(set(info[1:]))
                    
                    # print(tuple_info, type(tuple_info), info, type(info))
                    
                    data[key].append(tuple(temp))
        print(data)
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


