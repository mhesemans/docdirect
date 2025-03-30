from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import News


# Create your views here.
class NewsList(generic.ListView):
    queryset = News.objects.filter(status=1).order_by("-created_on")
    template_name = "news/index.html"
    paginate_by = 6


def news_detail(request, slug):
    """
    Display an individual :model:`news.News`.

    **Context**

    ``news``
        An instance of :model:`news.News`.

    **Template:**

    :template:`news/news_detail.html`
    """

    queryset = News.objects.filter(status=1)
    news = get_object_or_404(queryset, slug=slug)

    return render(
        request,
        "news/news_detail.html",
        {"news": news},
    )
