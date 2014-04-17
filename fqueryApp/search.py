from collections import defaultdict 
from fquery import settings
from models import Status, Comment, Photo, Link, Note, Video, Post
import queryProcess, index


CONTENT_TYPE_STATUS         = 1
CONTENT_TYPE_POST           = 1 << 1
CONTENT_TYPE_COMMENT        = 1 << 2
CONTENT_TYPE_LINK           = 1 << 3
CONTENT_TYPE_PHOTO          = 1 << 4
CONTENT_TYPE_NOTE           = 1 << 5
CONTENT_TYPE_VIDEO          = 1 << 6
CONTENT_TYPE_QUESTION       = 1 << 7
CONTENT_TYPE_QUESTION_OPTION = 1 << 8


CONTENT_TYPE_LIST = [CONTENT_TYPE_STATUS, CONTENT_TYPE_POST, CONTENT_TYPE_COMMENT,CONTENT_TYPE_LINK, CONTENT_TYPE_PHOTO ]


stopwords = queryProcess.importStopwords()

######## tokenizing ###########
def tokenize_status(fb_owner_id, selected_friends):
    tokens_lst = defaultdict(dict)

    docs_all = Status.objects.none()
    for friend_id in selected_friends:
        docs_all = docs_all|Status.objects.filter(status_from_id = friend_id)

    docs_all = docs_all.filter(owner_id = fb_owner_id)

    num_docs  = docs_all.count()
    for status in docs_all:
        tokens = queryProcess.processLine(status.status_message)
        for token in tokens:
            tokens_lst[token][status.status_id] = tokens_lst.get(token, {}).get(status.status_id, 0) + 1

    return tokens_lst, num_docs

def tokenize_comment(fb_owner_id, selected_friends):
    tokens_lst = defaultdict(dict)

    docs_all = Comment.objects.filter(owner_id = fb_owner_id)
    num_docs  = docs_all.count()
    for comment in docs_all:
        tokens = queryProcess.processLine(comment.comment_message)
        for token in tokens:
            tokens_lst[token][comment.comment_id] = tokens_lst.get(token, {}).get(comment.comment_id, 0) + 1
    return tokens_lst, num_docs

def tokenize_post(fb_owner_id, selected_friends):
    tokens_lst = defaultdict(dict)
    docs_all = Post.objects.filter(owner_id = fb_owner_id)
    num_docs  = docs_all.count()
    for post in docs_all:
        #print "id", post.post_id
        #print "caption:", post.post_caption
        #print "description:", post.post_description
        #print "message:", post.post_message
        #print "story:", post.post_story
        #print "name:", post.post_name
        #print "link:", post.post_link
        tokens = queryProcess.processLine(
            post.post_caption + ' '+  post.post_description + ' '+ post.post_message + ' '+ 
            post.post_story + ' '+ post.post_name)
        for token in tokens:
            tokens_lst[token][post.post_id] = tokens_lst.get(token, {}).get(post.post_id, 0) + 1

    return tokens_lst, num_docs

def tokenize_link(fb_owner_id, selected_friends):
    tokens_lst = defaultdict(dict)

    docs_all = Link.objects.filter(owner_id = fb_owner_id)
    num_docs  = docs_all.count()
    for link in docs_all:
        tokens = queryProcess.processLine(link.link_name + ' '+ link.link_description + ' '+ link.link_message)
        for token in tokens:
            tokens_lst[token][link.link_id] = tokens_lst.get(token, {}).get(link.link_id, 0) + 1
    return tokens_lst, num_docs
    

def tokenize_photo(fb_owner_id, selected_friends):
    tokens_lst = defaultdict(dict)

    docs_all = Photo.objects.filter(owner_id = fb_owner_id)
    num_docs  = docs_all.count()
    for photo in docs_all:
        tokens = queryProcess.processLine(photo.photo_name)
        for token in tokens:
            tokens_lst[token][photo.photo_id] = tokens_lst.get(token, {}).get(photo.photo_id, 0) + 1
    return tokens_lst, num_docs

token_funcs_g = {
    CONTENT_TYPE_STATUS : tokenize_status,
    CONTENT_TYPE_COMMENT : tokenize_comment,
    CONTENT_TYPE_POST : tokenize_post,
    CONTENT_TYPE_LINK : tokenize_link,
    CONTENT_TYPE_PHOTO : tokenize_photo,
    }

def get_tokens(owner_id, selected_friends, c_type):
    tokens_lst = defaultdict(dict)
    num_docs = 0

    if c_type in token_funcs_g:
        return token_funcs_g[c_type](owner_id, selected_friends)

    return [tokens_lst, num_docs]


######## results ###########
def get_statuses(doc_set):
    results = {}
    i = 0
    for doc_no in sorted(doc_set, key = doc_set.get, reverse= True):
        statuses = Status.objects.filter(status_id = str(doc_no))
        results[i] = {}
        for status in statuses:
            results[i]["msg"] = status.status_message
            i += 1
    return results

def get_comments(doc_set):
    results = {}
    i = 0
    for doc_no in sorted(doc_set, key = doc_set.get, reverse= True):
        comments = Comment.objects.filter(comment_id = str(doc_no))
        results[i] = {}
        for comment in comments:
            results[i]["msg"] = comment.comment_message
            i += 1
    return results

def get_posts(doc_set):
    results = {}
    i = 0
    for doc_no in sorted(doc_set, key = doc_set.get, reverse= True):
        posts = Post.objects.filter(post_id = str(doc_no))
        results[i] = {}
        for post in posts:
            if post.post_link:
                results[i]["msg"] = post.post_story + "|" + post.post_description
                results[i]["url"] = post.post_link
            elif post.post_message:
                results[i]["msg"] = post.post_story + "|" + post.post_message
                results[i]["desc"] = post.post_description
            else:
                results[i]["msg"] = post.post_story
                results[i]["desc"] =  post.post_description

            i += 1
    return results

def get_links(doc_set):
    results = {}
    i = 0
    for doc_no in sorted(doc_set, key = doc_set.get, reverse= True):
        links = Link.objects.filter(link_id = str(doc_no))
        results[i] = {}
        for link in links:
            results[i]["msg"] = link.link_name
            results[i]["url"] = link.link_link
            i += 1
    return results

def get_photos(doc_set):
    results = {}
    i = 0
    for doc_no in sorted(doc_set, key = doc_set.get, reverse= True):
        photos = Photo.objects.filter(photo_id = str(doc_no))
        results[i] = {}
        for photo in photos:
            results[i]["msg"] = photo.photo_name
            results[i]["url"] = photo.photo_link
            i += 1
    return results

result_funcs_g = {
    CONTENT_TYPE_STATUS : get_statuses,
    CONTENT_TYPE_COMMENT : get_comments,
    CONTENT_TYPE_POST : get_posts,
    CONTENT_TYPE_LINK : get_links,
    CONTENT_TYPE_PHOTO : get_photos,
    }

def get_results(doc_set, c_type):

    results = [] 

    if c_type in result_funcs_g:
        return result_funcs_g[c_type](doc_set)

    return results

def apply_search(owner_id, selected_friends, query, c_type):

    # tokens_lst is a dictionary of token and its occurrences in document
    # Each word is mapped to a list of (document number, document frequency) pair
    # for example, if token A occurs once in document number 1 and 9, and twice in 4
    # its entry in tokens_lst would be ['A': (1,1), (4,2), (9,1)]

    tokens_lst = defaultdict(dict)

    [tokens_lst, num_docs] = get_tokens(owner_id, selected_friends, c_type)

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


    results = get_results(doc_set, c_type)


    return results


def get_relevant_contents(owner_id, selected_friends, query, content_type):

    content_dict = {}

    for c_type in CONTENT_TYPE_LIST:

        if ((content_type & c_type) == c_type):
            content_dict[c_type] = apply_search(owner_id, selected_friends, query, c_type)

    return content_dict
