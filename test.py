

def tokenize(TextFilePath):
    file = open(TextFilePath)
    token = []

    for line in file:
        for word in line.split(" "):
            word = word.lower()
            token.append(word)
    
    print(token)

TextFilePath = "C:\\Users\\ailee\\Desktop\\in4matx 141\\testA.txt"
tokenize(TextFilePath)