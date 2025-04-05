from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import News
from .forms import NewsPostForm


class NewsList(generic.ListView):
    """
    Displays a list of published news articles.

    **Context**
    ``news_list``: A queryset of :model:`news.News` filtered by status and ordered by creation date.

    **Template**
    :template:`news/index.html`
    """
    queryset = News.objects.filter(status=1).order_by("-created_on")
    template_name = "news/index.html"
    paginate_by = 6


def news_detail(request, slug):
    """
    Displays an individual news article.

    **Context**
    ``news``: An instance of :model:`news.News`.

    **Template**
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
    Checks whether the user is authenticated and belongs to the 'Administrative Staff' group,
    or is a superuser.

    :param user: Django User instance.
    :return: Boolean indicating if user has permission to post news.
    """
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name="Administrative Staff").exists()
    )


@user_passes_test(is_admin_staff, login_url='/')
def post_news(request):
    """
    Allows administrative staff or superusers to post news articles via a frontend form.

    **Context**
    ``form``: An instance of :form:`news.NewsPostForm`.

    **Template**
    :template:`news/post_news.html`
    """
    if request.method == "POST":
        form = NewsPostForm(request.POST)
        if form.is_valid():
            news_item = form.save(commit=False)
            news_item.author = request.user  # Optional: track who submitted
            news_item.save()
            messages.success(request, "News post created successfully.")
            return redirect("home")
    else:
        form = NewsPostForm()

    return render(request, "news/post_news.html", {"form": form})
