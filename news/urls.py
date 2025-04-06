from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # News homepage (used as home page)
    path('', views.NewsList.as_view(), name='home'),

    # Public news listing page
    path('articles/', views.news_post_list, name='news_post_list'),

    # News submission form
    path('post/', views.post_news, name='post_news'),

    # Edit a specific news post
    path('edit/<slug:slug>/', views.edit_news, name='edit_news'),

    # Delete a specific news post
    path('delete/<slug:slug>/', views.delete_news, name='delete_news'),

    # Individual news post detail
    path('<slug:slug>/', views.news_detail, name='news_detail'),
]
