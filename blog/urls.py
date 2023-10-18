from django.urls import path
from . import views


urlpatterns = [
    path('post/create/', views.CreatePost.as_view(), name='post_create'),
    path('', views.Index.as_view(), name='index'),
    path('post/<int:id>', views.PostDetailView.as_view(), name='post_details'),
    path('comment/<int:id>', views.update, name='comment_update'),
    path('delete/<int:id>', views.delete, name='comment_delete'),
]

