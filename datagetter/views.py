from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
import db_controller
# Create your views here.
from django.http import HttpResponse


def index(request):

    context = RequestContext(request)
    posts = db_controller.get_post_data()
    context_dict = {'boldmessage': "Craigs Data Grabber will go here...",
                    'posts': posts}

    return render_to_response('datagetter/index.html', context_dict, context)

    # return HttpResponse("Craigs Data Grabber will go here...")