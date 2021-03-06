from __future__ import print_function
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
import db_controller
import data_grabber
# Create your views here.
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):

    context = RequestContext(request)
    posts = db_controller.get_post_data()
    context_dict = {'boldmessage': "Craigs Data Grabber will go here...",
                    'posts': posts}

    return render_to_response('datagetter/index.html', context_dict, context)

    # return HttpResponse("Craigs Data Grabber will go here...")


def new_index(request):

    context = RequestContext(request)
    posts = db_controller.get_post_data(without_ratings=True)
    context_dict = {'boldmessage': "Craigs Data Grabber will go here...",
                    'posts': posts, 'type': 'new'}

    return render_to_response('datagetter/new_index.html', context_dict, context)


def saved_posts(request):
    context = RequestContext(request)
    posts = db_controller.get_post_data(without_ratings=False, saved=True)
    context_dict = {'boldmessage': "Craigs Data Grabber will go here...",
                    'posts': posts, 'type': 'saved'}

    return render_to_response('datagetter/new_index.html', context_dict, context)


def all_posts(request):
    context = RequestContext(request)
    posts = db_controller.get_post_data(without_ratings=False, saved=False)
    context_dict = {'boldmessage': "Craigs Data Grabber will go here...",
                    'posts': posts, 'type': 'all'}

    return render_to_response('datagetter/new_index.html', context_dict, context)


def mobile_index(request):

    context = RequestContext(request)

    context_dict = {'boldmessage': "Craigs Mobile Data Grabber will go here..."}

    return render_to_response('datagetter/mobile.html', context_dict, context)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def rate_post(request):
    post_id = request.POST.get('post_id', '')
    rating_type = request.POST.get('rating_type', '')

    like_post = None
    if rating_type == 'like':
        like_post = True
    elif rating_type == 'dislike':
        like_post = False

    print('i received the following value: {0}, type: {1}'.format(post_id, like_post), end="\n\n\n")

    db_controller.rate_posting(post_id, like_post)

    return HttpResponse(json.dumps({'message': 'success'}), content_type="application/json")



@csrf_exempt
@require_http_methods(["GET", "POST"])
def get_count(request):
    post_count, save_count = db_controller.get_count_of_new_listings()
    return HttpResponse(json.dumps({'message': 'success', 'post_count': post_count, 'save_count': save_count}),
                        content_type="application/json")


@csrf_exempt
@require_http_methods(["GET", "POST"])
def delete_post(request):

    print('made it to del post view....')

    post_id = request.POST.get('post_id', '')

    print('i received the following value: {0}'.format(post_id), end="\n\n\n")

    db_controller.delete_posting(post_id)

    return HttpResponse(json.dumps({'message': 'success'}), content_type="application/json")


def refresh_posts(request):

    print('made it to refresh view....')
    data_grabber.refresh_all_postings()
    print('all done!')

    return HttpResponse(json.dumps({'message': 'success'}), content_type="application/json")