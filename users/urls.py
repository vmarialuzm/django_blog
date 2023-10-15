from django.contrib.auth import views as auth_views
from django.urls import path
from .views import RegisterView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]