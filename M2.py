<<<<<<< HEAD
from Retrieval import load_data


if __name__ ==  "__main__":
    url_data = load_data('url_ids.csv', ',')
    word_data = load_data('word_index_locator.csv', ',')

    print("URL Data:")
    print(url_data)
    print("\nWord Data:")
    print(word_data)
=======

from QueryObject import *
from Query import *
from Ranking import *



if __name__ ==  "__main__":
    database = QueryDB()
    query1 = Query(database)
    query1.querying()
>>>>>>> aa4dfc13af83a88c67135f5c36ec2186bf3a632d
