# websockets/urls.py
from os import name
from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:game_room>/<str:user_name>/', views.game_room, name="game_room")
]