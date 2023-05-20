from QueryObject import *
from Query import *
from Ranking import *
import itertools  # for slicing dictionary

if __name__ ==  "__main__":
    database = QueryDB()
    query1 = Query(database)
    query1.querying()
    
    # loop through all words in the query to get score set of all postings having that word
    # score_list has the form:
    # {
    #     word: {doc:score, doc:score, doc:score},
    #     word: {doc:score, doc:score}
    # }
    score_list = {}
    for word in query1.query:
        word_rank = Ranker(word, query1)
        word_rank.getscore()
        score_list[word] = word_rank.score
    
    # get query tfidf score
    query_score = get_tf_idf_of_query_words(query1.query, query1)
    #dictionary format of score of words in query for all urls having them
    # {
    #     url1: {score_w1, score_w2, score_w3},
    #     url2: {score_w1, score_w2, score_w3},
    #     url3: {score_w1, score_w2, score_w3},
    # }
    all_doc_vector = {}
    for word in query1.query:
        for url in query1.parent.url_id_to_string:
            if url in score_list[word]:
                if url in all_doc_vector:
                    all_doc_vector[url].append(score_list[word][url])
                else:
                    all_doc_vector[url] = []
                    all_doc_vector[url].append(score_list[word][url])

    # add score 0 to words not appear in url but appears in query
    for url in all_doc_vector:
        if len(all_doc_vector[url]) < len(query1.query):
            for i in range(len(query1.query) - len(all_doc_vector[url])):
                all_doc_vector[url].append(0)
        
        
    # the dictionary of cosine similarities score for all docs containing at least 1 word in the query
    cos_sim_list = {}    
    for doc in all_doc_vector:
        cos_sim = compute_cosine_similarities(query_score, all_doc_vector[doc])
        cos_sim_list[doc] = cos_sim
        #print(f"{doc} : {cos_sim}")
    
    # sort the cosine similarities score dictionaries
    cos_sim_list = sorturl(cos_sim_list)
    
    # take the top 5 urls
    if len(cos_sim_list) >= 5:
        top5 = dict(itertools.islice(cos_sim_list.items(), 5))
    else:
        top5 = cos_sim_list
        
    
    # output the top 5 urls
    for k,v in top5.items():
        print(query1.parent.url_id_to_string[k])  
    