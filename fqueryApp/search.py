from collections import defaultdict 
from fquery import settings
from models import Status, Comment, Photo, Link, Note, Video, Post
import queryProcess, index


CONTENT_TYPE_STATUS         = 1
CONTENT_TYPE_COMMENT        = 1 << 1
CONTENT_TYPE_LINK           = 1 << 2
CONTENT_TYPE_PHOTO          = 1 << 3
CONTENT_TYPE_NOTE           = 1 << 4
CONTENT_TYPE_POST           = 1 << 5
CONTENT_TYPE_VIDEO          = 1 << 6
CONTENT_TYPE_QUESTION       = 1 << 7
CONTENT_TYPE_QUESTION_OPTION = 1 << 8


stopwords = queryProcess.importStopwords()

def get_tokens(content_type):
    # =========== Extract Token Set ============ #
    # query_set = Status.objects.none()
    # for word in query.split():
    #     if word in stopwords:
    #         continue
    #     word = queryProcess.stemword(word)
    #     query_set = query_set| Status.objects.filter(status_message__contains = word)

    tokens_lst = defaultdict(dict)
    num_docs = 0

    if ((content_type & CONTENT_TYPE_STATUS) == CONTENT_TYPE_STATUS):
        status_all = Status.objects.all()
        num_docs  = Status.objects.count()
        for status in status_all:
            tokens = queryProcess.processLine(status.status_message)
            for token in tokens:
                tokens_lst[token][status.status_id] = tokens_lst.get(token, {}).get(status.status_id, 0) + 1

    return [tokens_lst, num_docs]

def get_results(doc_set, content_type):

    results = []

    if ((content_type & CONTENT_TYPE_STATUS) == CONTENT_TYPE_STATUS):
        for doc_no in sorted(doc_set, key = doc_set.get, reverse= True):
            statuses = Status.objects.filter(status_id = str(doc_no))
            for status in statuses:
                results.append(status.status_message)

    return results

def apply_search(query, content_type):

    # for testing purpose
    content_type = CONTENT_TYPE_STATUS

    # tokens_lst is a dictionary of token and its occurrences in document
    # Each word is mapped to a list of (document number, document frequency) pair
    # for example, if token A occurs once in document number 1 and 9, and twice in 4
    # its entry in tokens_lst would be ['A': (1,1), (4,2), (9,1)]

    tokens_lst = defaultdict(dict)

    [tokens_lst, num_docs] = get_tokens(content_type)

    # eliminate stopwords and stemming
    tokens_lst = queryProcess.stemmer(tokens_lst, stopwords)

    # ===== Applying weighting scheme ===== #

    # doc_freq_lst maps token to its document frequency
    doc_freq_lst = dict()
    for token, doc_list in tokens_lst.items(): 
        doc_freq_lst[token] = len(doc_list)

    weight_index = index.calcWeight(tokens_lst, num_docs)
    doc_length = index.calcDocLen(weight_index)


    # =========== Process the Query ============ #
    query_doc_no = 1

    query_tokens_lst = defaultdict(dict) 
    # tokenize the query
    tokens = queryProcess.processLine(query)

    for token in tokens:
        query_tokens_lst[token][query_doc_no] = query_tokens_lst.get(token, {}).get(query_doc_no, 0) + 1
    # stem and eliminate stopwords
    query_tokens_lst = queryProcess.stemmer(query_tokens_lst, stopwords)

    # ========== Extract Query Set ============ #
    query = query.lower()

    # doc_set maps each document to its similarity score with the query
    doc_set = dict()

    # query_set is the set of items that contain at least one term in the query

    for term in query_tokens_lst:
        for doc_no in tokens_lst[term]:
            # initialize the similarity score to 0
            if doc_no not in doc_set:
                doc_set[doc_no] = 0

    # calculate term weight and query length
    query_weight_index = index.calcQueryWeight(doc_freq_lst, query_tokens_lst, num_docs)
    query_length = index.calcDocLen(query_weight_index)
            
    # Calculate the cosine similarity

        # Accumulate the inner product
    for term in query_tokens_lst:
        for doc_no in doc_set:
            doc_set[doc_no] = doc_set[doc_no] + weight_index[term].get(doc_no, 0) * query_weight_index[term][query_doc_no]

        # Normalize using document length
    for doc_no in doc_set:

        doc_set[doc_no] = doc_set[doc_no]/(doc_length[doc_no] * query_length[query_doc_no])


    results = get_results(doc_set, content_type)


    return results



