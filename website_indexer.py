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
from collections import defaultdict

from PartA import tokenizeHTMLString, computeWordFrequencies
import string
from sys import argv
import time
from bs4 import BeautifulSoup
import lxml


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


# merge token files
def merge_files(output_file):
    #  with open(output_file, "w") as out_file:
    #      for file in sorted(os.listdir("Tokens"), key=lambda x: x.lower()):
    #          if file.endswith(".txt"):
    #              with open(f"Tokens/{file}", "r") as in_file:
    #                  for line in in_file:
    #                      out_file.write(line)
    #              os.remove(f"Tokens/{file}")
    lines = []

    for file in sorted(os.listdir("Tokens"), key=lambda x: x.lower()):
        if file.endswith(".txt"):
            with open(f"Tokens/{file}", "r") as in_file:
                lines.extend(in_file.readlines())
            os.remove(f"Tokens/{file}")

    with open(output_file, "w", buffering=8192) as out_file:
        out_file.writelines(lines)


def file_parser(main_folder):
    unique_word = set()
    url_ids = dict()
    word_url = defaultdict(list)
    url_no = 0
    document_count = 0
    line_no = 0 #track line number of word on website_index.txt after writing to it
    word_line = dict() # map word with its line_no

    important_text = dict()

    # read the main folder and loop through all the sub folders
    for folder in os.listdir(main_folder):
        # merges the path
        folder = os.path.join(main_folder, folder)
        # read the sub folder and loop through all the files
        for file in os.listdir(folder):
            # checks the file has a json extension
            try:
                if file.endswith(".json"):
                    with open(os.path.join(folder, file), "r") as f:
                        data = json.load(f)
                        # call function to add the url to a file
                        
                        #content parsing - extract html tags
                        # CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
                        # words = re.sub(CLEANR, ' ', data["content"])
                        words = BeautifulSoup(data["content"], "lxml").text
                        
                        words_list = tokenizeHTMLString(words)
                        print(words_list)
                        frequencies = computeWordFrequencies(words_list)

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
                        for word, frequency in frequencies.items():
                            url_info.addWordInfo(word, ["regular", frequency])

                        for word, frequency in special_case_frequencies.items():
                            url_info.addWordInfo(word, ["special_case", frequency])

                        for word, info in url_info.getWordInfo().items():
                            organized_info = ""
                            position = set()
                            for i in range(len(words_list)):
                                if words_list[i] == word:
                                    position.add(i)
                            if len(info) > 1:
                                organized_info += f"{url_no},{info[0][1]},{info[1][1]},{position}"
                            else:
                                organized_info += f"{url_no},{info[0][1]},0, {position}"
                            unique_word.add(word)
                            word_url[word].append(organized_info)

                            # linecache.clearcache()
                        # print(url_no)
                        # for word in frequencies:
                        #    if word not in word_locations:
                        #       word_locations[word] = line
                        #       #index.write(word + ": " + data["url"] + "\n")
                        #       index.write(f"{word} : {{{data['url']}, {frequencies[word]}}}\n")
                        #       line += 1
                        #    else:
                        #       current_line = 0

                        #       while current_line != word_locations[word]:
                        #          #current_line_info = index.readline().strip()
                        #          current_line+=1

                        #       current_line_info = linecache.getline(r"website_index.txt", current_line)
                        #       print(word + ": " + str(current_line))
                        #       print(current_line_info)
                        #       #current_line_info = index.readline()
                        #       # putting urls with the same word into the same line.
                        #       # 1st idea is to add to the end of the line we find it with
                        #       # 2nd idea is to create a lot of text files each with a word then merge it at the end haha

                        #       word_locations[word] = line
                        #       print(data["url"])
                        #       index.write(f"{current_line_info.strip()}, {{{data['url']}, {frequencies[word]}}}\n")
                        #       #index.write(f"{word} : ({data['url']}, {frequencies[word]})\n")
                        #       line += 1
                        #       linecache.clearcache()

                    f.close()
                    document_count += 1
                    url_no += 1
            except json.JSONDecodeError as e:
                print(f"File {file} is not a valid json file")
                continue
    with open("website_index.csv", "w", encoding='utf-8', newline='') as f,\
            open("word_index_locator.csv", "w", encoding='utf-8', newline='') as t:
        writer_f = csv.writer(f)
        writer_t = csv.writer(t)
        line_no = 0
        for word, details in sorted(word_url.items()):
            print(word, details)
            line_no += 1
            writer_f.writerow([word, details])
            writer_t.writerow([word, line_no])
    f.close()
    t.close()
    with open("url_ids.csv", "w", encoding='utf-8', newline='') as f:
        writer_f = csv.writer(f)
        for id, url in url_ids.items():
            writer_f.writerow([id, url])
    f.close()
    with open("count.txt", "w") as f:
        f.write(str(document_count))
    f.close()
    #print(word_line)

if __name__ == "__main__":
   #  file_parser("/Users/lanceli/Downloads/inlab3/cs121/CS121_Assignment3/ANALYST")
   #  file_parser("C:/Users/Anthony Wen/Downloads/CS121_Assignment3/analyst/ANALYST")
    print(f"starting at: {start_time}")
    file_parser("/Users/lanceli/Downloads/inlab3/cs121/CS121_Assignment3/TEMP")
    print("--- %s seconds ---" % (time.time() - start_time))