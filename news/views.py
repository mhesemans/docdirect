from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_news(request):
    return HttpResponse("Hello, this is news!")