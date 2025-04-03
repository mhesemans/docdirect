from django.shortcuts import render
from news.models import News

def home_view(request):
    latest_news = News.objects.filter(status=1).order_by('-created_on').first()
    return render(request, "home/home.html", {
        'latest_news': latest_news
    })
