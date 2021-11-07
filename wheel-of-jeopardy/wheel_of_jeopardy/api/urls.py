# api/urls.py
from django.conf.urls import url
from django.urls import path

from api import views

urlpatterns = [
    path('category', views.get_category, name='category'),
    path('question', views.get_question, name='question'),
    path('register', views.register_user, name='register'),
    path('unregister', views.unregister_user, name='unregister'),
    path('validate', views.validate_answer, name='validate'),
    path('table', views.get_user_table, name='table'),
    path('generate', views.generate_game, name="generate_game"),
    path('remaining', views.get_remaining_questions, name="get_remaining_questions"),
    path('active', views.get_active_player, name="get_active_player"),
]