from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path('home', views.home, name='homepage'),
    path('', views.index, name='home'),
    path('find', views.find, name='find'),
    path('terms', views.terms, name='terms'),
    path('about', views.about, name='about'),
    path('profile', views.profile, name='profile'),
    path('login', views.signin, name='login'),
    path('signup', views.signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
]
