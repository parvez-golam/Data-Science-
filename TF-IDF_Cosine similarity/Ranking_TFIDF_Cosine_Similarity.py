#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
# Name: Parvez Golam
# Date: 27/02/2021
# Retrieval of top 10 documents based on 
# TF-IDF & cosine similarity for ranking
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

import os
import glob
import math

# Returns all the text documents present in 'path'
def load_docs(fpath):
    doc_list = []

    for filename in glob.glob(os.path.join(fpath, '*.txt')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            docname = filename.split( "\\")
            data = f.read()
            item = ( docname[1], data)
            doc_list.append(item)

    return doc_list

# Counts frequency of each word in 'word_list'
# returns a dictionary which maps the words to  their frequency
def count_frequency(word_list):
    d = {}  

    for word in word_list:
        if word in d: 
            d[word] = d[word] + 1       
        else: 
            d[word] = 1          
    return d 

# Prints top 'n' most popular words from dictionary 'word_count_dic'
# containing word and word counts
def most_frequent( word_count_dic , n):
    sorted_t = sorted(word_count_dic.items(), key=lambda v:v[1], reverse=True)   

    print("Top %d most popular words are:" %n)
    for i in range(n) :
        print(sorted_t[i][0], ':', sorted_t[i][1])   
    
    print("\nWords with min. size 4 and max. size 20 are :")
    counter = 0
    for k,v in sorted_t:
        if (len(k) <= 20) and (len(k) >= 4) and (counter < n):
            counter += 1
            print (k, ':', v)

# Computes TF for words in each doc, 
# DF for all words in all docs
def process_docs(all_docs):
    all_words = []                                          
    counts_dict = {}                                      

    # - counts words in a doc
    # - collects doc data, word and word-counts
    #   {'d1' : {'a': 1, 'b':6} }
    # - collects all words from each doc
    for doc in all_docs:                    
        words_counted = count_frequency(doc[1].split())          
        counts_dict[doc[0]] = words_counted                 
        all_words = all_words + doc[1].split()  
                                
    # DF of all unique words from each doc, counted  
    word_freq = count_frequency(all_words)              
    
    return word_freq, counts_dict 
 
# Computes TF-IDF for all words in all docs
# from 'doc_dict'-fequency of the words in a each document
# and 'df_counts'- total frequency of words from all documents
def compute_tfidf(doc_dict, df_counts):
    #Dict that will hold tf-idf matrix
    tfidf_dict = {} 
    no_of_doc = len(doc_dict)

    #for each doc
    # - get all the unique words in the doc
    # - calculate  TF-IDF scores for each word
    # - store all TF-IDF scores for words with doc_name
    for doc_name in doc_dict:                              
        doc_words = doc_dict[doc_name].keys()              
        wd_tfidf_scores = {}

        #for each word in the doc
        # - get the word counts dict for the doc
        # - compute TF-IDF
        # - store TF-IDF scores with word
        for wd in list(set(doc_words)):                      
            wds_tf = doc_dict[doc_name]                     
            wd_tfidf = wds_tf[wd] * (math.log(no_of_doc/df_counts[wd],2) + 1)  
            wd_tfidf_scores[wd] = round(wd_tfidf, 4)  

        tfidf_dict[doc_name] = wd_tfidf_scores  

    return tfidf_dict
   
# returns the dot product of two documents 
def inner_product(d1, d2):  
    sum = 0.0

    for k in d1:    
        if k in d2: 
            sum += (d1[k] * d2[k]) 
       
    return sum

# Calculates cosine similarity for a document in 'doc_name'
# with other documents based on TF-IDF stored in 'doc_tfidf_dict'
# Assumption: entered document is among the documents available
def get_cosine_similarity(doc_name, doc_tfidf_dict):
    # get the entered document details
    vec1 = doc_tfidf_dict[doc_name]
    doc_cosine_sim = {}
    cosine_scores = {}

    # Compute the Cosine-similarity of the documents 'doc_name'
    for k in doc_tfidf_dict.keys(): 
        vec2 = doc_tfidf_dict[k]
        numerator = inner_product(vec1, vec2) 
        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        if not denominator:
            cosine_scores[k] = 0.0
        else:
            cosine_scores[k] = round(float(numerator) / denominator, 3)
    
    doc_cosine_sim[doc_name] =  cosine_scores

    return doc_cosine_sim


# Driver function that takes document name, file path and retrieval number(k)
# and prints the top k relevant documents of 'doc_name' with cosine score,
# from given path 'fpath'
def retrieve_documents(doc_name, fpath, k):
    # Get all the documents from a file path
    all_docs = load_docs(fpath)

    # Get total frequency of words from all documents and
    # fequency of the words in a each document
    word_freq, vector_dict = process_docs(all_docs)

    # most popular words (top 200)
    most_frequent(word_freq, 200)  

    # Get TF-IDF for all words in all docs
    tfidf_matrix = compute_tfidf(vector_dict,  word_freq ) 

    # Get Cosine similarty for the document
    cosine_sim = get_cosine_similarity( doc_name, tfidf_matrix)

    # Print top k relevant documents with cosine score
    for key,value in cosine_sim.items():
        sorted_docs = sorted(value.items(), key=lambda v:v[1], reverse=True)
        relavant_docs = [sorted_docs[r] for r in range(k)]
        print("\nTop %d relevant documents for documemnt %s are :" %(k, key))
        print(relavant_docs)


#--Driver Program 

# diectory path where all documents are avialable
path = "C:/Users/admin/Desktop/Dataset"
# Entered document
document = "101.txt"
# retrive top 10 revant document from 'path' 
retrieve_documents(document, path, 10 )
