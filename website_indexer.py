######################################################################################################################
# functionality:
#    for each website, find all the words in the content and use each word as a key and add the url to its value
# input:
#   a folder containing json files
# output:
#   a text file where it starts with the key then ":" then [urls]
# example outputs
#   apple: [apple.com, appleAreNice.com]
#   pineapple: [pineapple.com, pineappleAreNice.com]
######################################################################################################################
# team members:
# Aileen Tran aileenyt, 79192463
# Anthony Wen awen5, 62858003
# Van Pham vantp2, 74369428
# Lance Li lancekl, 90653176
######################################################################################################################
import csv
import os
import json
import sys
from collections import defaultdict
from itertools import islice

from PartA import tokenizeHTMLString, computeWordPosition, computeWordFrequencies
import string
import time
from bs4 import BeautifulSoup
import lxml
import threading


class urlWordInfo:
    def __init__(self):
        self.word_info = defaultdict(list)

    def addWordInfo(self, word, word_info):
        self.word_info[word].append(word_info)

    def getWordInfo(self):
        return self.word_info

start_time = time.time()

# create Tokens folder for token files
if not os.path.exists('Tokens'):
    os.makedirs('Tokens')


def write_token_to_file(token, url, frequency):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    token_name = ''.join(c if c in valid_chars else '_' for c in token)

    filename = f"Tokens/{token_name}.txt"
    with open(filename, "a") as file:
        file.write(f"{{{url}: {frequency}}}\n")




def count_json_files(folder_path):
    count = 0

    # Traverse the directory tree using os.walk()
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.json'):
                count += 1

    return count


def file_parser(main_folder):
    unique_word = set()
    url_ids = dict()
    word_url = defaultdict(list)
    url_no = 0
    document_count = 0
    word_locator = defaultdict(lambda: [-1, -1, -1])  # map word with its line_no

    total_count_file = count_json_files(main_folder)
    first_second_stop = int(total_count_file / 3)
    split_count = 0
    print(first_second_stop)

    # read the main folder and loop through all the sub folders
    for folder in os.listdir(main_folder):
        # print(folder)
        # merges the path
        folder = os.path.join(main_folder, folder)
        # read the sub folder and loop through all the files
        for file in os.listdir(folder):
            # checks the file has a json extension
            # print(file)
            try:
                if file.endswith(".json"):
                    with open(os.path.join(folder, file), "r") as f:
                        data = json.load(f)
                        # call function to add the url to a file

                        # content parsing - extract html tags
                        # CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
                        # words = re.sub(CLEANR, ' ', data["content"])
                        words = BeautifulSoup(data["content"], "lxml").text

                        words_list = tokenizeHTMLString(words)
                        position = computeWordPosition(words_list)

                        # hash the url
                        # url_id = hash(data["url"])
                        # add the url to the id dictionary
                        url_ids[url_no] = data["url"]

                        # getting important text from content
                        soup = BeautifulSoup(data["content"], 'lxml')
                        tags = ['b', 'strong', 'h1', 'h2', 'h3', 'title']
                        special_case = [tag.text for tag in soup.find_all(tags)]
                        special_case_list = tokenizeHTMLString(" ".join(special_case))
                        special_case_frequencies = computeWordFrequencies(special_case_list)

                        url_info = urlWordInfo()
                        for word, frequency in position.items():
                            url_info.addWordInfo(word, ["regular", len(frequency), frequency])

                        for word, frequency in special_case_frequencies.items():
                            if word not in url_info.getWordInfo():
                                url_info.addWordInfo(word, ["regular", 0, set()])
                            url_info.addWordInfo(word, ["special_case", frequency])
                        for word, info in url_info.getWordInfo().items():

                            organized_info = ""
                            if len(info) > 1:
                                organized_info += f"{url_no},{info[0][1]},{info[1][1]},{len(words_list)},{info[0][2]}"
                            else:

                                organized_info += f"{url_no},{info[0][1]},0,{len(words_list)},{info[0][2]}"
                            unique_word.add(word)
                            word_url[word].append(organized_info)


                        # splitter
                        if split_count < 2:
                            if document_count / first_second_stop > 0 and document_count % first_second_stop == 0:
                                split_count += 1
                                with open(f"website_index_{split_count}.csv", "w", encoding='utf-8', newline='') as index:
                                    writer_index = csv.writer(index)
                                    line_no = 0
                                    for word, details in sorted(word_url.items()):
                                        line_no += 1
                                        writer_index.writerow([word, details])
                                        word_locator[word][split_count-1] = line_no
                                index.close()
                                word_url.clear()

                        elif split_count == 2:
                            if document_count == total_count_file:
                                split_count += 1
                                with open(f"website_index_{split_count}.csv", "w", encoding='utf-8', newline='') as index:
                                    writer_index = csv.writer(index)
                                    line_no = 0
                                    for word, details in sorted(word_url.items()):
                                        line_no += 1
                                        writer_index.writerow([word, details])
                                        word_locator[word][split_count-1] = line_no
                                index.close()
                                word_url.clear()

                    f.close()
                    document_count += 1
                    url_no += 1
            except json.JSONDecodeError as e:
                print(f"File {file} is not a valid json file")
                continue

    with open("word_index_locator.csv", "w", encoding='utf-8', newline='') as t:
        writer_t = csv.writer(t)
        for word, details in sorted(word_locator.items()):
            writer_t.writerow([word, details])
    t.close()

    csv.field_size_limit(100000000)
    with open(f"website_index.csv", "w", encoding='utf-8', newline='') as full_index, \
            open(f"website_index_0.csv", "r", encoding='utf-8', newline='') as index1, \
            open(f"website_index_1.csv", "r", encoding='utf-8', newline='') as index2, \
            open(f"website_index_2.csv", "r", encoding='utf-8', newline='') as index3:
        writer_index = csv.writer(full_index)

        index1_reader = csv.reader(index1)
        index2_reader = csv.reader(index2)
        index3_reader = csv.reader(index3)
        word1 = "0"
        word2 = "0"
        word3 = "0"
        value1 = eval(next(index1_reader)[1])
        value2 = eval(next(index2_reader)[1])
        value3 = eval(next(index3_reader)[1])
        value1_done = False
        value2_done = False
        value3_done = False

        for word, details in sorted(word_locator.items()):

            all_values = set()

            try:
                # Iterate through each line in the CSV file
                while word1 < word and not value1_done:
                    nextLine1 = next(index1_reader)
                    word1 = eval(nextLine1[0])
                    value1 = eval(nextLine1[1])
                if word1 == word:
                    for url in value1:
                        all_values.add(url)
            except StopIteration:
                value1_done = True

            try:
                # Iterate through each line in the CSV file
                while word2 < word and not value2_done:
                    nextLine2 = next(index2_reader)
                    word2 = nextLine2[0]
                    value2 = eval(nextLine2[1])
                if word2 == word:
                    for url in value2:
                        all_values.add(url)
            except StopIteration:
                value2_done = True

            try:
                # Iterate through each line in the CSV file
                while word3 < word and not value3_done:
                    nextLine3 = next(index3_reader)
                    word3 = nextLine3[0]
                    value3 = eval(nextLine3[1])
                if word3 == word:
                    for url in value3:
                        all_values.add(url)
            except StopIteration:
                value3_done = True

            writer_index.writerow([word, all_values])
    full_index.close()
    index1.close()
    index2.close()
    index3.close()

    with open("url_ids.csv", "w", encoding='utf-8', newline='') as f:
        writer_f = csv.writer(f)
        for id, url in url_ids.items():
            writer_f.writerow([id, url])
    f.close()
    with open("count.txt", "w") as f:
        f.write(str(document_count))
    f.close()
    # print(word_line)



# merge token files
def merge_files(locator):
    #  with open(output_file, "w") as out_file:
    #      for file in sorted(os.listdir("Tokens"), key=lambda x: x.lower()):
    #          if file.endswith(".txt"):
    #              with open(f"Tokens/{file}", "r") as in_file:
    #                  for line in in_file:
    #                      out_file.write(line)
    #              os.remove(f"Tokens/{file}")
    lines = []
    csv.field_size_limit(100000000)
    with open(locator) as locator_file, open(f"website_index.csv", "w", encoding='utf-8', newline='') as full_index, \
        open(f"website_index_1.csv", "r", encoding='utf-8', newline='') as index2, \
        open(f"website_index_2.csv", "r", encoding='utf-8', newline='') as index3:
        writer_index = csv.writer(full_index)


        locator = csv.reader(locator_file)
        # index1_reader = csv.reader(index1)
        index2_reader = csv.reader(index2)
        index3_reader = csv.reader(index3)
        # word1 = "0"
        word2 = "0"
        word3 = "0"
        # value1 = eval(next(index1_reader)[1])
        value2 = eval(next(index2_reader)[1])
        value3 = eval(next(index3_reader)[1])
        # value1_done = False
        value2_done = False
        value3_done = False


        for line in locator:

            # Extract values from the line
            word = line[0]
            all_values = set()

            # try:
            #     # Iterate through each line in the CSV file
            #     while word1 < word and not value1_done:
            #         nextLine1 = next(index1_reader)
            #         word1 = eval(nextLine1[0])
            #         value1 = eval(nextLine1[1])
            #     if word1 == word:
            #         for url in value1:
            #             all_values.add(url)
            # except StopIteration:
            #     value1_done = True

            try:
                # Iterate through each line in the CSV file
                while word2 < word and not value2_done:
                    nextLine2 = next(index2_reader)
                    word2 = nextLine2[0]
                    value2 = eval(nextLine2[1])
                if word2 == word:
                    for url in value2:
                        all_values.add(url)
            except StopIteration:
                value2_done = True

            try:
                # Iterate through each line in the CSV file
                while word3 < word and not value3_done:
                    nextLine3 = next(index3_reader)
                    word3 = nextLine3[0]
                    value3 = eval(nextLine3[1])
                if word3 == word:
                    for url in value3:
                        all_values.add(url)
            except StopIteration:
                value3_done = True


            writer_index.writerow([word, all_values])



if __name__ == "__main__":

    print(f"starting at: {start_time}")
    # print(count_json_files("C:/Users/Lilan/Documents/CS121_Assignment3/DEV"))
    file_parser("C:/Users/Lilan/Documents/CS121_Assignment3/DEV")
    # merge_files("word_index_locator.csv")



    print("--- %s seconds ---" % (time.time() - start_time))