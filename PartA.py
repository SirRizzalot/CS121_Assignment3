

#runtime complexity explanation linear? polynomial? exponential? 
#[delete later] token: sequence of alphanumeric characters indepednent of
#capitalization

#List<Token> tokenize(TextFilePath)
def tokenize(TextFilePath):
    file = open(TextFilePath)
    token = []

    for line in file:
        for word in line.split(" "):
            word = word.lower()
            token.append(word)
    #setToken = {token}
    return list(set(token))


TextFilePath = "C:\\Users\\ailee\\Desktop\\in4matx 141\\testA.txt"


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


print(computeWordFrequencies(tokenize(TextFilePath)))
#void print(Frequencies<Token,Count>)