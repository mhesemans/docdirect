from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    # Homepage-style news feed (only latest few articles, used on main home page)
    path('', views.NewsList.as_view(), name='home'),

    # Public-facing news article list page
    path('articles/', views.news_post_list, name='news_post_list'),

    # Form page to allow admin staff to submit news
    path('post/', views.post_news, name='post_news'),

    # Detail view for a single article using slug in URL
    path('<slug:slug>/', views.news_detail, name='news_detail'),
]
