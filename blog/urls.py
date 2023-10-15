from django.urls import path
from . import views


urlpatterns = [
    path('post/create/', views.CreatePost.as_view(), name='post_create'),
    path('', views.Index.as_view(), name='index'),
]

