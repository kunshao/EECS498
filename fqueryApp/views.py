# Create your views here.
from django.shortcuts import render,render_to_response
from django.template import RequestContext,loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import simplejson

from fqueryApp.models import Status, Comment, Photo, Link, Note, Video, Post, Question, QuestionOption

from fqueryApp import search
from fquery import settings
 

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
    json_data = simplejson.load(request)
    owner_id = json_data['owner_id']
    query_str = json_data['query']
    content_flags = int(json_data['content_flags'])
    selected_friends = json_data['friend_list']

    relevant_content = search.get_relevant_contents(owner_id, selected_friends,
            query_str, content_flags)

    data_obj = {
        'data' : relevant_content
    }
    return HttpResponse(simplejson.dumps(data_obj), content_type = "text/json")

    

@csrf_exempt
def save_statuses(request):
    json_data = simplejson.load(request)
    local_save_statuses(json_data['status_list'], json_data['fb_owner_id'])
    return HttpResponse("Finished storing statuses for user")

def local_save_statuses(status_arrary, fb_owner_id):
    for json_obj in status_arrary:
        status, created = Status.objects.get_or_create(status_id = json_obj['id'])
        status.status_from_id = json_obj['from']['id']
        status.owner_id = fb_owner_id
        if ('message' in json_obj):
            status.status_message = json_obj['message'].encode('ascii', 'ignore')
        status.status_updated_time = json_obj['updated_time']
        if ('comments' in json_obj):
            local_save_comments(json_obj['comments']['data'], fb_owner_id)
        status.save()


@csrf_exempt
def save_posts(request):
    json_data = simplejson.load(request)
    local_save_posts(json_data['post_list'], json_data['fb_owner_id'])
    return HttpResponse("Finished storing statuses for user")


def local_save_posts(post_array, fb_owner_id):
    for json_obj in post_array:
        print "post id: " + str(json_obj['id'])
        post, created = Post.objects.get_or_create(post_id = json_obj['id'])
        if ('caption' in json_obj):
            post.post_caption = json_obj['caption'].encode('ascii', 'ignore')

        if ('description' in json_obj):
            post.post_description = json_obj['description'].encode('ascii', 'ignore')
        
        if ('message' in json_obj):
            post.post_message = json_obj['message'].encode('ascii', 'ignore')

        if ('name' in json_obj):
            post.post_name = json_obj['name'].encode('ascii', 'ignore')

        if ('story' in json_obj):
            post.post_story = json_obj['story'].encode('ascii', 'ignore')

        if ('link' in json_obj):
            post.post_story = json_obj['link']

        post.post_from_id = json_obj['from']['id']
        post.owner_id = fb_owner_id

        post.post_updated_time = json_obj['updated_time']
        if ('comments' in json_obj):
            local_save_comments(json_obj['comments']['data'], fb_owner_id)
        post.save()


@csrf_exempt
def save_photos(request):
    json_data = simplejson.load(request)
    local_save_photos(json_data['photo_list'], json_data['fb_owner_id'])
    return HttpResponse("Finished storing pictures for user")

def local_save_photos(array, fb_owner_id):
    print 'local_save_pictures'
    
    for json_obj in array:

        photo_obj, created = Photo.objects.get_or_create(photo_id = json_obj['id'])
        photo_obj.photo_from_id = json_obj['from']['id']
        photo_obj.owner_id = fb_owner_id
        photo_obj.photo_link = json_obj['link']
        if ('name' in json_obj):
            photo_obj.photo_name = json_obj['name']
        photo_obj.photo_created_time = json_obj['created_time']
        if ('comments' in json_obj):
            local_save_comments(json_obj['comments']['data'], fb_owner_id)
        photo_obj.save()


@csrf_exempt
def save_notes(request):
    print 'save_notes'
    json_data = simplejson.load(request)
    local_save_notes(json_data['note_list'], json_data['fb_owner_id'])
    return HttpResponse("Finished storing pictures for user")

def local_save_notes(array, fb_owner_id):
    print 'local_save_notes'
    
    for json_obj in array:

        note_obj, created = Note.objects.get_or_create(note_id = json_obj['id'])
        note_obj.note_created_time = json_obj['created_time']
        note_obj.note_from_id = json_obj['from']['id']
        note_obj.owner_id = fb_owner_id
        
        if ('message' in json_obj):
            note_obj.note_message = json_obj['message'].encode('ascii', 'ignore')

        if ('subject' in json_obj):
            note_obj.note_subject = json_obj['subject']

        if ('updated_time' in json_obj):
            note_obj.note_updated_time = json_obj['updated_time']


        if ('comments' in json_obj):
            local_save_comments(json_obj['comments']['data'], fb_owner_id)
        note_obj.save()

def local_save_comments(array, fb_owner_id):
    for json_obj in array:
        comment_obj, created = Comment.objects.get_or_create(comment_id = json_obj['id'])
        comment_obj.owner_id = fb_owner_id
        comment_obj.comment_from_id = json_obj['from']['id']
        comment_obj.comment_message = json_obj['message'].encode('ascii', 'ignore')
        comment_obj.comment_created_time = json_obj['created_time']
        comment_obj.save()


@csrf_exempt
def save_links(request):
    json_data = simplejson.load(request)
    local_save_links(json_data['link_list'], json_data['fb_owner_id'])
    return HttpResponse("Finished storing links for user")

def local_save_links(array, fb_owner_id):
    for json_obj in array:

        link_obj, created = Link.objects.get_or_create(link_id = json_obj['id'])
        link_obj.link_created_time = json_obj['created_time']
        
        if ('description' in json_obj):
            link_obj.link_description = json_obj['description'].encode('ascii', 'ignore')

        link_obj.link_from_id = json_obj['from']['id']
        link_obj.owner_id = fb_owner_id
        if ('link' in json_obj):
            link_obj.link_link = json_obj['link'].encode('ascii', 'ignore')
        if ('message' in json_obj):
            link_obj.link_message = json_obj['message'].encode('ascii', 'ignore')
        if ('name' in json_obj):
            link_obj.link_name = json_obj['name'].encode('ascii', 'ignore')
        if ('comments' in json_obj):
            local_save_comments(json_obj['comments']['data'], fb_owner_id)
        link_obj.save()


def index(request):
    status_list = Status.objects.all()
    template = loader.get_template('status/index.html')
    context = RequestContext(request, {
            'status_list': status_list,})
    return HttpResponse(template.render(context))
