from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import News
from .forms import NewsPostForm


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


def is_admin_staff(user):
    """
    Check if a user is in the 'Administrative Staff' group.
    """
    return user.groups.filter(name="Administrative Staff").exists()


@login_required
@user_passes_test(is_admin_staff)
def post_news(request):
    """
    Allows administrative staff to create news posts through a frontend form.

    **Context**
    ``form``
        An instance of :form:`news.NewsPostForm` for creating a news item.

    **Template:**
    :template:`news/post_news.html`
    """
    if request.method == "POST":
        form = NewsPostForm(request.POST)
        if form.is_valid():
            news_item = form.save(commit=False)
            news_item.save()
            messages.success(request, "News post created successfully.")
            return redirect("post-news")
    else:
        form = NewsPostForm()

    return render(request, "news/post_news.html", {"form": form})
