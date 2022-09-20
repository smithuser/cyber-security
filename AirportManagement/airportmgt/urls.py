from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='show_index'),
    path('login/', views.show_login, name='show_login'),
    path('register/', views.show_signup, name='show_signup'),
    path('auth/0/', views.login, name='login'),
    path('auth/0/register', views.signup, name='signup'),
    path('auth/0/logout', views.logout, name='logout'),
]