from collections import defaultdict 
import math


def calcWeight(tokens_lst, N):  

    # tf_idf_index is a dictionary that maps each term to its (doc_no, weight) tuple
    tf_idf_index = defaultdict(dict)

    for token, doc_list in tokens_lst.items():
        doc_freq = len(doc_list)
        for doc_no, term_freq in doc_list.items():
            tf_idf = term_freq * math.log10(float(N)/doc_freq)
            tf_idf_index[token][doc_no] = tf_idf_index.get(token, {}).get(doc_no, 0.0) + tf_idf

    return tf_idf_index

def calcQueryWeight(doc_freq_lst, tokens_lst, N):   
    # tf_idf_index is a dictionary that maps each term to its (doc_no, weight) tuple
    tf_idf_index = defaultdict(dict)

    for token, doc_list in tokens_lst.items():
        for doc_no, term_freq in doc_list.items():
            if token not in doc_freq_lst:
                tf_idf = 0
            else:
                doc_freq = doc_freq_lst[token]
                tf_idf = term_freq * math.log10(float(N)/doc_freq)
            tf_idf_index[token][doc_no] = tf_idf_index.get(token, {}).get(doc_no, 0.0) + tf_idf

    return tf_idf_index


def calcDocLen(tf_idf_index):
    # doc_length maps document number to its document length
    doc_length = dict()

    # take the sum of all term_weight^2
    for token, doc_list in tf_idf_index.items():
        for doc_no, term_weight in doc_list.items():
            doc_length[doc_no] = doc_length.get(doc_no, 0.0) + math.pow(term_weight, 2)

    # then take the square root
    for doc_no in doc_length:
        doc_length[doc_no] = math.pow(doc_length[doc_no], 0.5)
    return doc_length