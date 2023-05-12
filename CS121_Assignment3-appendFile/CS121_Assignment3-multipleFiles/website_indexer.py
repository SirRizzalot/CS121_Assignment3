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
# Lance Li - 90653176
# Anthony Wen - 62858003
# Van Pham - 74369428
# Aileen Tran - 79192463
######################################################################################################################
import os
import json
from collections import defaultdict
import big_o
from PartA import tokenizeHTMLString, computeWordFrequencies
import string
from sys import argv
import time
from bs4 import BeautifulSoup

#adds important info to url_info dictionary 
class urlWordInfo:
    def __init__(self):
        self.word_info = defaultdict(list)

    #adds type of word to value list
    def addWordInfo(self, word, word_info):
        self.word_info[word].append(word_info)

    #returns dictionary of keys: unique words values: list of list containing type of word and frequency 
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
    lines = []

    for file in sorted(os.listdir("Tokens"), key=lambda x: x.lower()):
        if file.endswith(".txt"):
            with open(f"Tokens/{file}", "r") as in_file:
                lines.extend(in_file.readlines())
            os.remove(f"Tokens/{file}")

    with open(output_file, "w", buffering=8192) as out_file:
        out_file.writelines(lines)


def file_parser(main_folder):

    unique_word = set() # words in content no duplicates
    url_ids = dict() 
    word_url = defaultdict(list) 
    url_no = 0
    document_count = 0
    line_no = 0 #track line number of word on website_index.txt after writing to it
    word_line = dict() # map word with its line_no

    important_text = dict()

    # read the main folder and loop through all the sub folders
    # taking O(n)
    for folder in os.listdir(main_folder):
        # merges the path
        folder = os.path.join(main_folder, folder)
        # read the sub folder and loop through all the files
        #nested loop O(n^2)
        for file in os.listdir(folder):
            # checks the file has a json extension
            try:
                if file.endswith(".json"):
                    with open(os.path.join(folder, file), "r") as f:
                        data = json.load(f)
                        # call function to add the url to a file
                        
                        # creates unique hash id for url
                        # url_id = hash(data["url"])
                        # add the url to the url_id dictionary
                        url_ids[url_no] = data["url"]
                        url_no += 1

                        #pulls word content from json file using lxml parser
                        words = BeautifulSoup(data["content"], "lxml").text
                        
                        #takes the word list stems and tokenizes the word
                        words_list = tokenizeHTMLString(words)
                        
                        #frequency = {"word": str, "value": frequency}
                        frequencies = computeWordFrequencies(words_list)
                        
                        
                        # getting important text from content
                        soup = BeautifulSoup(data["content"], 'lxml')
                        
                        #tags indicating important text
                        tags = ['b', 'strong', 'h1', 'h2', 'h3', 'title']
                        #finds tags and stores the text associated with them
                        special_case = [tag.text for tag in soup.find_all(tags)]
                        special_case_list = tokenizeHTMLString(" ".join(special_case))
                        #counts frequency of special words saves to dictionary
                        special_case_frequencies = computeWordFrequencies(special_case_list)
                        
                        url_info = urlWordInfo()

                        #adds regular and special words and their frequencies to url_info
                        for word, frequency in frequencies.items():
                            url_info.addWordInfo(word, ["regular", frequency])
                            
                        for word, frequency in special_case_frequencies.items():
                            url_info.addWordInfo(word, ["special_case", frequency])
                        
                        #organizes list so it is arranged by url_id, regular word freq, special word freq
                        #then adds it as the value to the word in word_url dictionary
                        for word, info in url_info.getWordInfo().items():
                            print("w ", word, " i ", info)
                            organized_info = ""
                            if len(info) > 1:
                                
                                organized_info += f"{url_no}:{info[0][1]},{info[1][1]}"
                                
                            else:
                                organized_info += f"{url_no}:{info[0][1]}"
                            unique_word.add(word)
                            word_url[word].append(organized_info)
                        
                        
                           

                    f.close()
                    document_count += 1
            except json.JSONDecodeError as e:
                print(f"File {file} is not a valid json file")
                continue
    with open("website_index.txt", "w", encoding='utf-8') as f, open("word_index_locator.txt", "w", encoding='utf-8') as t:
        line_no = 0
        for word, details in sorted(word_url.items()):
            line_no += 1
            f.write(f"{word}: {details}\n")
            t.write(f"{word} : {line_no}\n")
    f.close()
    t.close()
    with open("url_ids.txt", "w") as f:
        for id, url in url_ids.items():
            f.write(f'{{{id}: {url}}}\n')
    f.close()
    with open("count.txt", "w") as f:
        f.write(str(document_count))
    f.close()
    #print(word_line)

if __name__ == "__main__":
   #  file_parser("/Users/lanceli/Downloads/inlab3/cs121/CS121_Assignment3/ANALYST")
   #  file_parser("C:/Users/Anthony Wen/Downloads/CS121_Assignment3/analyst/ANALYST")
    file_parser("C:/Users/ailee/Desktop/in4matx 141/CS121_Assignment3-appendFile/CS121_Assignment3-multipleFiles/TEMP")
    #file_parser("/Users/lanceli/Downloads/inlab3/cs121/CS121_Assignment3/DEV")
    print("--- %s seconds ---" % (time.time() - start_time))
    