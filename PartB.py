import PartA
import time
import re
import sys
def intersect_two_files(file1, file2):
    count = 0
    freq_file1 = PartA.computeWordFrequencies(PartA.tokenize(file1))
    freq_file2 = PartA.computeWordFrequencies(PartA.tokenize(file2))
    for key in freq_file1:
        
        if key in freq_file2:
            print(key)
            count = count + 1
    return count

def main():
   
    TextFilePath1 = sys.argv[1]
    TextFilePath2 = sys.argv[2]
    count = intersect_two_files(TextFilePath1, TextFilePath2)
    print(count)
    
if __name__ == "__main__":
    main()