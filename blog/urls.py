from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('post/create/', views.CreatePost.as_view(), name='post_create'),
    path('', views.Index.as_view(), name='index'),
    path('post/<int:id>/', views.PostDetailView.as_view(), name='post_details'),
    path('post/update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('comment/<int:id>/', views.update, name='comment_update'),
    path('delete/<int:id>/', views.delete, name='comment_delete'),
    path('post/like/<int:post_id>/', views.like_post, name='like_post'),
    path('post/disliked/<int:post_id>/', views.disliked_post, name='disliked_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
