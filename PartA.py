import re
import time
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
        print(token)
        return token
    except FileNotFoundError as e:
        print("File not found")

start_time = time.time()
TextFilePath = "C:\\Users\\ailee\\Desktop\\in4matx 141\\testA.txt"
tokenize(TextFilePath)
stop_time = time.time() 
print(stop_time-start_time)
#Map<Token,Count> computeWordFrequencies(List,Token>)

def computeWordFrequencies(token_list):
    map_token = dict()
    for word in token_list:
        if word in map_token:
            value = map_token(word)
            map_token[word] = value+1 
        else:
            map_token[word] = 1
    return map_token


#map_token = computeWordFrequencies(tokenize(TextFilePath))
#print(map_token)
#void print(Frequencies<Token,Count>)
#def Frequencies(map_token):
#    print(list(map_token))

#print(Frequencies(map_token))