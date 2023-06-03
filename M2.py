from QueryObject import *
from Query import *
from Ranking import *
import itertools  # for slicing dictionary
import time


######################################################################################################################
# team members:
# Aileen Tran aileenyt, 79192463
# Anthony Wen awen5, 62858003
# Van Pham vantp2, 74369428
# Lance Li lancekl, 90653176
######################################################################################################################
if __name__ ==  "__main__":
    database = QueryDB()
    query1 = Query(database)
    query1.querying()
    
    # loop through all words in the query to get score set of all postings having that word
    # score_list and special_score_list has the form:
    # {
    #     word: {doc:score, doc:score, doc:score},
    #     word: {doc:score, doc:score}
    # }
    start = time.time()
    score_list = {}  # tfidf scores
    #dictionary format of score of words in query for all urls having them
    # {
    #     url1: {score_w1, score_w2, score_w3},
    #     url2: {score_w1, score_w2, score_w3},
    #     url3: {score_w1, score_w2, score_w3},
    # }
    all_doc_vector = {}
    top_urls = {}  #storing urls with high special words weight
    top_urls_for_tfidf = [] #storing urls with high tfidf points
    start2 = time.time()
    for word in query1.query:
        word_rank = Ranker(word, query1)
        # get tfidf score
        word_rank.getTFIDF()
        score_list[word] = word_rank.tfidf_score
        
        # make top_score_list and top_special_score_list to get top urls with highest score     
        if len(score_list[word]) >= 20:
            sorted_dict = dict(sorted(score_list[word].items(), key=lambda x: x[1], reverse=True))
            top_score_list = dict(list(sorted_dict.items())[:20])
        else:
            top_score_list = score_list[word]
            
        #make top_urls to combine top_score_list and top_special_score_list
        for url, score in top_score_list.items():
            top_urls[url] = score
                
        
        for url in top_urls:
            if url in all_doc_vector:
                all_doc_vector[url].append(top_urls[url])
            else:
                all_doc_vector[url] = []
                all_doc_vector[url].append(top_urls[url])
    end2 = time.time()
    
    start3 = time.time()
    # get query tfidf score
    query_score = get_tf_idf_of_query_words(query1.query, query1)
    end3 = time.time()
    
    # add score 0 to words not appear in url but appears in query
    for url in all_doc_vector:
        if len(all_doc_vector[url]) < len(query1.query):
            for i in range(len(query1.query) - len(all_doc_vector[url])):
                all_doc_vector[url].append(0)
        
    start4 = time.time()
    # # take the top 5 urls
    # if len(top_urls) >= 10:
    #     top_urls = dict(itertools.islice(top_urls.items(), 10))
    # else:
    #     top_urls = top_urls
    # the dictionary of cosine similarities score for all docs containing at least 1 word in the query
    cos_sim_list = {}    
    count = 0
    for doc in top_urls:
        print(count)
        count += 1
        cos_sim = compute_cosine_similarities(query_score, all_doc_vector[doc])
        cos_sim_list[doc] = cos_sim
    end4 = time.time()
      
       
    start6 = time.time() 
    # sort the cosine similarities score dictionaries
    cos_sim_list = sorturl(cos_sim_list)
    #print("cos_sim_list", cos_sim_list)
    # take the top 5 urls
    if len(cos_sim_list) >= 5:
        top5 = dict(itertools.islice(cos_sim_list.items(), 5))
    else:
        top5 = cos_sim_list
    
    end6 = time.time()    
    
    # output the top 5 urls
    for k,v in top5.items():
        print(query1.parent.url_id_to_string[k])  
    end = time.time()
    print("time", end - start)
    print("time do word_rank", end2 - start2)
    print("time calculate tfidf of query", end3 - start3)
    print("time calculate cosine", end4 - start4)
    print("time sort", end6 - start6)