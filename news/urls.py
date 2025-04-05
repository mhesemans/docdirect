from django.urls import path
from . import views

urlpatterns = [
    # News homepage
    path('', views.NewsList.as_view(), name='home'),

    # News submission form
    path('post/', views.post_news, name='post_news'),

    # Full news post
    path('<slug:slug>/', views.news_detail, name='news_detail'),
]