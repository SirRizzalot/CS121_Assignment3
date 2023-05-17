############################################################
# load in data
# 1. determining weights
# 2. create scoring functions
# 3. compare scores
############################################################
from sklearn.feature_extraction.text import TfidfVectorizer
from PartA import tokenizeHTMLString

def compute_tf_idf_weight(doc, word_list):
    vectorizer = TfidfVectorizer(tokenizer=tokenizeHTMLString)
    
    # Compute the TF-IDF scores for the given document
    tfidf_matrix = vectorizer.fit_transform([doc])
    
    # Get the feature names (words)
    feature_names = vectorizer.get_feature_names_out()
    
    # Get the TF-IDF scores for the document
    tfidf_scores = tfidf_matrix.toarray()[0]
    
    # Create a dictionary to store the word and its corresponding TF-IDF score
    tfidf_dict = {}
    count = 1
    for word, score in zip(feature_names, tfidf_scores):
        tfidf_dict[word] = score
        count += 1
    
    print(count)
    return tfidf_dict