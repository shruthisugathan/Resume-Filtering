from django.urls import path
from .import views

urlpatterns = [
    path('',views.login),
    path('home',views.home),
    path('register',views.register),
    path('output',views.output),
    path('voice',views.voice),
    
]
