from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import News
from .forms import NewsPostForm


class NewsList(generic.ListView):
    """
    Displays a list of published news articles for the homepage.

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
    Displays a full individual news article.

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


def news_post_list(request):
    """
    Displays a list of all published news articles for the public-facing news page.

    **Context**
    ``news_list``: A queryset of :model:`news.News`.

    **Template**
    :template:`news/news_post.html`
    """
    news_list = News.objects.filter(status=1).order_by("-created_on")
    return render(request, "news/news_post.html", {"news_list": news_list})


def is_admin_staff(user):
    """
    Checks whether the user is authenticated and belongs to the 'Administrative Staff' group,
    or is a superuser.

    :param user: Django User instance.
    :return: Boolean indicating if user has permission to post/edit/delete news.
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
            news_item.author = request.user
            news_item.save()
            messages.success(request, "News post created successfully.")
            return redirect("news:news_post_list")
    else:
        form = NewsPostForm()

    return render(request, "news/post_news.html", {"form": form})


@login_required
@user_passes_test(is_admin_staff, login_url="/")
def edit_news(request, slug):
    """
    Allows admin staff or superusers to edit an existing news article.

    **Context**
    ``form``: A bound instance of :form:`news.NewsPostForm`.

    **Template**
    :template:`news/post_news.html`
    """
    news_item = get_object_or_404(News, slug=slug)

    if request.method == "POST":
        form = NewsPostForm(request.POST, instance=news_item)
        if form.is_valid():
            form.save()
            messages.success(request, "News article updated successfully.")
            return redirect("news:news_post_list")
    else:
        form = NewsPostForm(instance=news_item)

    return render(request, "news/post_news.html", {"form": form})


@login_required
@user_passes_test(is_admin_staff, login_url='/')
def delete_news(request, slug):
    """
    Allows administrative staff or superusers to delete an existing news post.

    **Template**
    :template:`news/confirm_delete.html`
    """
    news = get_object_or_404(News, slug=slug)

    if request.method == "POST":
        news.delete()
        messages.success(request, "News post deleted successfully.")
        return redirect("news:news_post_list")

    return render(request, "news/confirm_delete.html", {"news": news})
