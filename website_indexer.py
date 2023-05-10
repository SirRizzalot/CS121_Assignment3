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
from PartA import tokenizeHTMLString, computeWordFrequencies
import string
import linecache
from sys import argv
from itertools import islice


def file_parser(main_folder):

   word_locations = dict()
   url_ids = dict()
   line = 1

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
                  unique_words = tokenizeHTMLString(data["content"])
                  frequencies = computeWordFrequencies(unique_words)
                  
                  # hash the url
                  url_id = hash(data["url"])
                  # add the url to the id dictionary
                  url_ids[url_id] = data["url"]
                  index = open("website_index.txt", "a+")
                  for word in frequencies:
                     if word not in word_locations:
                        word_locations[word] = line
                        #index.write(word + ": " + data["url"] + "\n")
                        index.write(f"{word} : {{{data['url']}, {frequencies[word]}}}\n")
                        line += 1
                     else:
                        current_line = 0

                        while current_line != word_locations[word]:
                           #current_line_info = index.readline().strip()
                           current_line+=1
                        
                        current_line_info = linecache.getline(r"website_index.txt", current_line)
                        print(word + ": " + str(current_line))
                        print(current_line_info)
                        #current_line_info = index.readline()
                        # putting urls with the same word into the same line.
                        # 1st idea is to add to the end of the line we find it with
                        # 2nd idea is to create a lot of text files each with a word then merge it at the end haha
                        
                        word_locations[word] = line
                        print(data["url"])
                        index.write(f"{current_line_info.strip()}, {{{data['url']}, {frequencies[word]}}}\n")
                        #index.write(f"{word} : ({data['url']}, {frequencies[word]})\n")
                        line += 1
                        linecache.clearcache()
                        
               f.close()
                  
         except json.JSONDecodeError as e:
            print(f"File {file} is not a valid json file")
            continue

   print(word_locations)   


if __name__ == "__main__":
   file_parser("/Users/thyva.000/cs121/a3-m1/CS121_Assignment3/ANALYST")