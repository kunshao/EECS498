# Create your views here.
from django.shortcuts import render,render_to_response
from django.template import RequestContext,loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson

from fqueryApp.models import Status, Comment, Photo, Link, Note, Video, Post, Question, QuestionOption

from fqueryApp import search
from fquery import settings

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



# query is the string user puts down. content_type is 
def get_relevant_contents(query, content_type):

    content_dict = {}
 

    for c_type in CONTENT_TYPE_LIST:

        if ((content_type & c_type) == c_type):
            results_list = []
            results = search.apply_search(query, c_type)
            for result in results:
                results_list.append({'msg' : result})
            content_dict[c_type] = results_list


    # if ((content_type & CONTENT_TYPE_STATUS) == CONTENT_TYPE_STATUS):
    #     content_dict[CONTENT_TYPE_STATUS] = results_list

    return content_dict
    

def render_login(request):
    print 'render_login'
    return render_to_response('home/login.html', 
        {
            'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID
        }
    )

def home(request):
    print 'home'
    return render_to_response('home/home.html', 
        {
            'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID
        }
    )


@csrf_exempt
def make_query(request):
    query_str = request.GET['query']
    content_flags = int(request.GET['content_flags'])

    relevant_content = get_relevant_contents(query_str, content_flags)
    # json_obj = {}
    # num_content_flags = 9;
    # for i in xrange(0, num_content_flags):
    #     if ((1 << i) in relevant_content):
    #         json_obj_one_type_list = []
    #         for obj in relevant_content[1 << i]:
    #             one_msg = {
    #                 'msg' : obj[
    #             }
    #             json_obj_one_type_list.append(one_msg)
    #     json_obj[1 << i] = json_obj_one_type_list

    data_obj = {
        'data' : relevant_content
    }
    return HttpResponse(simplejson.dumps(data_obj), content_type = "text/json")

    

@csrf_exempt
def save_statuses(request):
    # print 'save_statuses'
    json_data = simplejson.load(request)
    local_save_statuses(json_data)
    return HttpResponse("Finished storing statuses for user")

def local_save_statuses(status_arrary):
    # print 'local_save_statuses'
    
    for json_obj in status_arrary:
        status, created = Status.objects.get_or_create(status_id = json_obj['id'])
        status.status_from_id = json_obj['from']['id']
        if ('message' in json_obj):
            status.status_message = json_obj['message'].encode('ascii', 'ignore')
        status.status_updated_time = json_obj['updated_time']
        if ('comments' in json_obj):
            local_save_comments(json_obj['comments']['data'])
        status.save()


@csrf_exempt
def save_posts(request):
    # print 'save_statuses'
    json_data = simplejson.load(request)
    local_save_posts(json_data)
    return HttpResponse("Finished storing statuses for user")


def local_save_posts(post_array):
    print 'local_save_posts'
    
    for json_obj in post_array:
        post, created = Post.objects.get_or_create(post_id = json_obj['id'])
        if ('caption' in json_obj):
            post.post_caption = json_obj['caption']

        if ('description' in json_obj):
            post.post_description = json_obj['description']
        
        if ('message' in json_obj):
            post.post_message = json_obj['message']

        if ('name' in json_obj):
            post.post_name = json_obj['name']

        if ('story' in json_obj):
            post.post_story = json_obj['story']


        post.post_from_id = json_obj['from']['id']

        post.post_updated_time = json_obj['updated_time']
        if ('comments' in json_obj):
            local_save_comments(json_obj['comments']['data'])
        # print 'json: ' + str(json_obj)
        if ('name' in json_obj):
            print 'json: ' + str(json_obj['name'])
            print 'obj: ' + str(post.post_name)
        post.save()


@csrf_exempt
def save_photos(request):
    # print 'save_pictures'
    json_data = simplejson.load(request)
    local_save_photos(json_data)
    return HttpResponse("Finished storing pictures for user")

def local_save_photos(array):
    print 'local_save_pictures'
    
    for json_obj in array:

        photo_obj, created = Photo.objects.get_or_create(photo_id = json_obj['id'])
        photo_obj.photo_from_id = json_obj['from']['id']
        photo_obj.photo_link = json_obj['link']
        if ('name' in json_obj):
            photo_obj.photo_name = json_obj['name']
        photo_obj.photo_created_time = json_obj['created_time']
        if ('comments' in json_obj):
            local_save_comments(json_obj['comments']['data'])
        photo_obj.save()


@csrf_exempt
def save_notes(request):
    print 'save_notes'
    json_data = simplejson.load(request)
    local_save_notes(json_data)
    return HttpResponse("Finished storing pictures for user")

def local_save_notes(array):
    print 'local_save_notes'
    
    for json_obj in array:

        note_obj, created = Note.objects.get_or_create(note_id = json_obj['id'])
        note_obj.note_created_time = json_obj['created_time']
        note_obj.note_from_id = json_obj['from']['id']
        
        if ('message' in json_obj):
            note_obj.note_message = json_obj['message']

        if ('subject' in json_obj):
            note_obj.note_subject = json_obj['subject']

        if ('updated_time' in json_obj):
            note_obj.note_updated_time = json_obj['updated_time']


        if ('comments' in json_obj):
            local_save_comments(json_obj['comments']['data'])
        note_obj.save()

def local_save_comments(array):
    # print 'local_save_comments'
    for json_obj in array:
        comment_obj, created = Comment.objects.get_or_create(comment_id = json_obj['id'])
        comment_obj.comment_from_id = json_obj['from']['id']
        comment_obj.comment_message = json_obj['message'].encode('ascii', 'ignore')
        comment_obj.comment_created_time = json_obj['created_time']
        comment_obj.save()


@csrf_exempt
def save_links(request):
    # print 'save_links'
    json_data = simplejson.load(request)
    local_save_links(json_data)
    return HttpResponse("Finished storing links for user")

def local_save_links(array):
    # print 'local_save_links'
    
    for json_obj in array:

        link_obj, created = Link.objects.get_or_create(link_id = json_obj['id'])
        link_obj.link_created_time = json_obj['created_time']
        
        if ('description' in json_obj):
            link_obj.link_description = json_obj['description']

        link_obj.link_from_id = json_obj['from']['id']
        link_obj.link_link = json_obj['link']
        if ('message' in json_obj):
            link_obj.link_message = json_obj['message'].encode('ascii', 'ignore')
        if ('name' in json_obj):
            link_obj.link_name = json_obj['name'].encode('ascii', 'ignore')
        if ('comments' in json_obj):
            local_save_comments(json_obj['comments']['data'])
        link_obj.save()









def index(request):
    status_list = Status.objects.all()
    template = loader.get_template('status/index.html')
    context = RequestContext(request, {
            'status_list': status_list,})
    return HttpResponse(template.render(context))
