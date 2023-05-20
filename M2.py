from QueryObject import *
from Query import *
from Ranking import *


if __name__ ==  "__main__":
    database = QueryDB()
    print(database.url_no)
    query1 = Query(database)
    query1.querying()
    score_list = {}
    # loop through all words in the query to get score set of all postings having that word
    # score_list has the form:
    # {
    #     word: {doc:score, doc:score, doc:score},
    #     word: {doc:score, doc:score}
    # }
    for word in query1.query:
        word_rank = Ranker(word, query1)
        word_rank.getscore()
        score_list[word] = word_rank.score
    
    # get query tfidf score
    query_score = get_tf_idf_of_query_words(query1.query, query1)
    print(query_score)
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
                #doc_score = get_tf_idf_of_a_doc(query_words, score_list, url)
                #cos_sim = compute_cosine_similarities(query_score, doc_score)
                #print(cos_sim)

    # add score 0 to words not appear in url but appears in query
    for url in all_doc_vector:
        if len(all_doc_vector[url]) < len(query1.query):
            for i in range(len(query1.query) - len(all_doc_vector[url])):
                all_doc_vector[url].append(0)
        
        
    for doc in all_doc_vector:
        cos_sim = compute_cosine_similarities(query_score, all_doc_vector[doc])
        print(f"{doc} : {cos_sim}")
    
