
from QueryObject import *
from Query import *
from Ranking import *



if __name__ ==  "__main__":
    database = QueryDB()
    query1 = Query(database)
    query1.querying()