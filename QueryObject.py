from collections import defaultdict
import csv


class QueryDB(object):

    def __init__(self):
        self.id_to_index = self.load_datatxt()
        self.url_id_to_string = self.load_urlId()
        self.Queries = list()
        self.words_locations = dict()
        self.url_no = len(self.url_id_to_string)

    def load_datatxt(self):
        data = {}
        with open('word_index_locator.txt') as file:
            for line in file:
                line = line.strip()
                key, value = line.split(' : ')
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


    def load_urlId(self):
        data = {}
        with open('url_ids.txt') as file:
            for line in file:
                line = line.strip()

                key, value = line[1:-1].split(': ')
                data[int(key)] = value
        return data

    def load_websitetxt(self, list_of_location):
        data = defaultdict(list)
        # keys = text.split()
        with open('website_index.txt') as file:
            counter = 1
            for word, location in list_of_location:
                if location == 0:
                    continue
                while counter < location:
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


