# api/urls.py
from django.conf.urls import url
from django.urls import path

from api import views

urlpatterns = [
    path('category', views.get_category, name='category'),
    path('question', views.get_question, name='question'),
    path('register', views.register_user, name='register'),
    path('unregister', views.unregister_user, name='unregister'),
    path('table', views.get_user_table, name='table' )
]