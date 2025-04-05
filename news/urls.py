from . import views
from django.urls import path

urlpatterns = [
    path('', views.NewsList.as_view(), name='home'),  # News homepage
    path('<slug:slug>/', views.news_detail, name='news_detail'),  # Full news post
    path('post/', views.post_news, name='post-news'),  # News submission form
]
