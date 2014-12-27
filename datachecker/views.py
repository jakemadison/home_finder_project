from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
# Create your views here.
from django.http import HttpResponse
# Create your views here.


def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': "Craigs Data Grabber will go here"}

    return render_to_response('datachecker/main.html', context_dict, context)
