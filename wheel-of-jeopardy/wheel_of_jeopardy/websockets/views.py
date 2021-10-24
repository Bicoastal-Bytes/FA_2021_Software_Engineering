import re
from django.shortcuts import render
from .forms import RegisterForm

# Create your views here.
def index(request):
    form = RegisterForm()
    return render(request, 'websockets/index.html', {'form': form})

def game_room(request, game_room, user_name):
    return render(request, 'websockets/game.html', {
        'game_room': game_room,
        'user_name': user_name,
    })
