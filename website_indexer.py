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
import string
from sys import argv


def file_parser(main_folder):
   for folder in os.listdir(main_folder):
      folder = os.path.join(main_folder, folder)
      for file in os.listdir(folder):
         if file.endswith(".json"):
            with open(os.path.join(folder, file), "r") as f:
               data = json.load(f)
               print(data["url"])



if __name__ == "__main__":
   file_parser("/Users/lanceli/Downloads/inlab3/cs121/CS121_Assignment3/ANALYST")