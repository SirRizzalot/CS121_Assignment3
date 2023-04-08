

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

TextFilePath = "C:\\Users\\ailee\\Desktop\\in4matx 141\\testA.txt"
tokenize(TextFilePath)

#Map<Token,Count> computeWordFrequencies(List,Token>)


#void print(Frequencies<Token,Count>)