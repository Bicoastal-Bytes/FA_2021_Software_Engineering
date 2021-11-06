# websockets/urls.py
from os import name
from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create_game, name='create_game'),
    path('join', views.join_game, name='join_game'),
    path('<str:game_room>/<str:user_name>/', views.game_room, name='game_room')
]