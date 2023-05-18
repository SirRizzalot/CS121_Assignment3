############################################################
# load in data
# 1. need to load in url_ids.txt -> dictionary
# 2. need to load in word_index_locator.txt  -> dictionary
# 3. given a specific line or lines, load in from website_index.txt
#    + needs to fast
#    + don't load in too much -> list of urls
############################################################
import csv

def load_data(file_name, separator):
    with open(file_name, mode='r') as infile:
        reader = csv.reader(infile)
        with open('coors_new.csv', mode='w') as outfile:
            writer = csv.writer(outfile)
            mydict = {rows[0]:rows[1] for rows in reader}
    return mydict

