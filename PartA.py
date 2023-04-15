import re
import time
import sys

#complexity is O(n^3) Polynomial time
#I read the file one line at a time and then split the line into words, I then split the words on special characters and add them to a list.
#one loop runs n amount of time,  second loop runs n times, third runs n times giving n^3

def tokenize(TextFilePath):
    token = []
    try:
        #utf8 read in non english characters
        with open(TextFilePath, encoding = "utf8") as file:
            for line in file:
                for word in line.split(" "):
                    if not word.isalnum():     
                        #splits any characters that are non alphanumeric                   
                        tempt_list = re.split(r"[^A-Z^a-z^0-9]", word)                        
                        tempt_list = [i for i in tempt_list if i.isalnum()]
                        token = token + tempt_list                       
                    else:
                        token.append(word)
        return token
    except FileNotFoundError as e:
        print("File not found")






#O(n) + O(n) = 2O(n) complexity = O(n)
#first for loop converts everything to lower case, second for loop adds words and frequencies to a map
def computeWordFrequencies(token_list):
    token_list = [i.lower() for i in token_list]
    map_token = dict()
    #words added to map_token frequence is 1, if the word is already in the map_token then frequence increases by 1
    for word in token_list:
        if word in map_token:
            map_token[word] = map_token.get(word) + 1
        else:
            map_token[word] = 1
    return map_token



#line 53 referenced from https://stackoverflow.com/questions/4233476/sort-a-list-by-multiple-attributes
#O(n) + O(n) + O(n log n) + O(n log n) => complexity = O(n log n)
#sort through words and frequencies twice O(n log n)
#list comprehension twice O(n)
def Frequencies(map_token):
    #creates a nested list with key and value having their own list
    list_items = [ [key, value] for key, value in map_token.items()]
    list_items.sort(key = lambda x: [x[0]])
    list_items.sort(key = lambda x: [x[1]], reverse = True)
    [print(f"{token[0]} - {token[1]}") for token in list_items]

#line 61 referenced from https://stackoverflow.com/questions/1009860/how-can-i-read-and-process-parse-command-line-arguments
def main():
    if len(sys.argv) != 2:
        print("Please provide a file to run")
    else: 
        TextFilePath = sys.argv[1]
        
        map_token = computeWordFrequencies(tokenize(TextFilePath))
        
        Frequencies(map_token)

if __name__ == "__main__":
    main()

