import pickle
import redis
from django.shortcuts import render
from .forms import RegisterForm, CreationForm

client = redis.client.StrictRedis()

# Create your views here.
def index(request):
    return render(request, 'websockets/index.html')

def create_game(request):
    form = CreationForm()
    return render(request, 'websockets/create_game.html', {'form': form})

def join_game(request):
    form = RegisterForm()
    if client.get('games') != None:
        available_games = pickle.loads(client.get('games'))
    else:
        available_games = []
    context = {
        'form': form,
        'games': available_games
    }
    return render(request, 'websockets/join_game.html', context)

def game_room(request, game_room, user_name):
    return render(request, 'websockets/game.html', {
        'game_room': game_room,
        'user_name': user_name,
    })
