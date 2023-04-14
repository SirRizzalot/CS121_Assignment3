import re
import time
import sys
#runtime complexity explanation linear? polynomial? exponential? 
#[delete later] token: sequence of alphanumeric characters indepednent of
#capitalization

#List<Token> tokenize(TextFilePath)
def tokenize(TextFilePath):
    token = []
    try:
        with open(TextFilePath) as file:
            for line in file:
                for word in line.split(" "):
                    if not word.isalnum():
                        tempt_list = re.split(r"[^A-Z^a-z^0-9]", word)
                        tempt_list = [i for i in tempt_list if i.isalnum()]
                        token = token + tempt_list
                        
                    else:
                        token.append(word)
        #setToken = {token}
        return token
    except FileNotFoundError as e:
        print("File not found")





#Map<Token,Count> computeWordFrequencies(List,Token>)

def computeWordFrequencies(token_list):
    token_list = [i.lower() for i in token_list]
    map_token = dict()
    # map key, value
    for word in token_list:
        if word in map_token:
            map_token[word] = map_token.get(word) + 1
        else:
            map_token[word] = 1
    return map_token



#line 53 referenced from https://stackoverflow.com/questions/4233476/sort-a-list-by-multiple-attributes

#print(map_token)
#void print(Frequencies<Token,Count>)
def Frequencies(map_token):
    #print(map_token)
    list_items = [ [key, value] for key, value in map_token.items()]
    list_items.sort(key = lambda x: [x[0]])
    list_items.sort(key = lambda x: [x[1]], reverse = True)
    [print(f"{token[0]} - {token[1]}") for token in list_items]

#line 61 referenced from https://stackoverflow.com/questions/1009860/how-can-i-read-and-process-parse-command-line-arguments
def main():
    start_time = time.time()

    TextFilePath = sys.argv[1]
    map_token = computeWordFrequencies(tokenize(TextFilePath))
    Frequencies(map_token)

    stop_time = time.time() 
    print(f"time {stop_time-start_time}")

if __name__ == "__main__":
    main()

