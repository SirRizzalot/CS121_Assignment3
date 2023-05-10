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
import time
start_time = time.time()

# create Tokens folder for token files
if not os.path.exists('Tokens'):
   os.makedirs('Tokens')
   
def write_token_to_file(token, url, frequency):
   valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
   token_name = ''.join(c if c in valid_chars else '_' for c in token)

   filename = f"Tokens/{token_name}.txt"
   with open(filename, "w") as file:
      file.write(f"{token}: {{{url}: {frequency}}}\n")
      
      
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
   url_no = 0

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
                  #url_id = hash(data["url"])
                  # add the url to the id dictionary
                  url_ids[url_no] = data["url"]
                  url_no += 1
                  #index = open("website_index.txt", "a+")
                  
                  for word, frequency in frequencies.items():
                     if word not in unique_word:
                        write_token_to_file(word, url_no, frequency)
                        unique_word.add(word)
                     else:
                        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
                        token_name = ''.join(c if c in valid_chars else '_' for c in word)
                        filename = f"Tokens/{token_name}.txt"
                        #current_line = linecache.getline(filename, 1)
                        
                        with open(filename, "r") as f:
                           current_line = f.readline()
                           # TEST
                           #print(word + " - " + current_line) 
                        
                           with open(filename, "w") as file:
                              file.write(f"{current_line.strip()[:-1]}, {url_no}: {frequencies[word]}}}\n")
                        
                        #linecache.clearcache()
                  print(url_no)      
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
   
   merge_files("website_index.txt")


if __name__ == "__main__":
   file_parser("/Users/thyva.000/cs121/a3-m1/CS121_Assignment3/ANALYST")
   print("--- %s seconds ---" % (time.time() - start_time))