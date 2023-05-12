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
import os
import json
from collections import defaultdict

from PartA import tokenizeHTMLString, computeWordFrequencies
import string
import linecache
from sys import argv
from itertools import islice
import time
# import urllib3
import urllib.request
from bs4 import BeautifulSoup
import sys

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
                        words_list = tokenizeHTMLString(data["content"])
                        frequencies = computeWordFrequencies(words_list)

                        # hash the url
                        # url_id = hash(data["url"])
                        # add the url to the id dictionary
                        url_ids[url_no] = data["url"]
                        url_no += 1
                        
                        # getting important text from content
                        soup = BeautifulSoup(data["content"], 'lxml')
                        tags = ['b', 'strong', 'h1', 'h2', 'h3', 'title']
                        text = [tag.text for tag in soup.find_all(tags)]
                        
                        # if(len(text) > 0):
                        #     print(text)
                        #     print(data["url"])
                        #     sys.exit()
                        
                        for words in text:
                            if words in important_text:
                                important_text[words] += 1
                            else:
                                important_text[words] = 1
                        # index = open("website_index.txtd", "a+")

                        for word, frequency in frequencies.items():
                            #print(word)
                            unique_word.add(word)
                            word_url[word].append([url_no, frequency])

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

            except json.JSONDecodeError as e:
                print(f"File {file} is not a valid json file")
                continue
    with open("website_index.txt", "w") as f:
        for word, details in sorted(word_url.items()):
            word_line[word] = line_no
            line_no += 1
            f.write(f"{word}: ")
            for detail in details:
                f.write(f"{{{detail[0]}, {detail[1]}}}, ")
            f.write("\n")
    with open("url_ids.txt", "w") as f:
        for id, url in url_ids.items():
            f.write(f'{{{id}: {url}}}\n')
    with open("important_text.txt", "w", encoding='utf-8') as f:
        for words, count in important_text.items():
            f.write(f'{{{words}: {count}}}\n')
    f.close()
    print(word_line)

if __name__ == "__main__":
   #  file_parser("/Users/lanceli/Downloads/inlab3/cs121/CS121_Assignment3/ANALYST")
   #  file_parser("C:/Users/Anthony Wen/Downloads/CS121_Assignment3/analyst/ANALYST")
    file_parser("C:/Users/thyva.000/cs121/a3-m1/CS121_Assignment3/TEMP")
    print("--- %s seconds ---" % (time.time() - start_time))