from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import ensure_csrf_cookie
from api.models import Category, Question, Choices
import random
import logging
from websockets.forms import RegisterForm, CreationForm
from websockets.tracking import UserTracker
import pickle
import redis
import json

logger = logging.getLogger(__name__)

client = redis.client.StrictRedis()

user_list = UserTracker()

room_list = []

# Create your views here.
def get_category(request):
    """Get a random category when called"""
    if request.method == "GET":
        logger.debug('Recieved a GET request for a category')
        categories = list(Category.objects.all())
        logger.debug('Getting all categories from database')
        random_categories = random.sample(categories, 1)
        logger.debug('Choosing a random category')
        random_category = random.choice(random_categories)
        logger.debug('Sending category back to user')
        return JsonResponse({'category': random_category.name})
    else:
        return HttpResponseNotAllowed(['GET'])

def get_question(request):
    """Get a question from a specific category and point value"""
    if request.method == 'GET':
        category = request.GET['category']
        points = request.GET['points']
        question = list(Question.objects.filter(category__name=category, point_value=points))
        logger.debug('Communicating with database to get question')
        choices = list(Choices.objects.filter(question_id=question[0].id))
        logger.debug('Communicating with database to get choices for question')
        response_data = {
            "question": question[0].question,
            "question_id": question[0].id,
            "choices": choices[0].choices,
            "choices_id": choices[0].id
        }
        logger.debug('Sending data back to client')
        remaining_questions = client.get("num_questions")
        remaining_questions -= 1
        client.set("num_questions", remaining_questions)
        return JsonResponse(response_data)
    else:
        return HttpResponseNotAllowed(['GET'])

def register_user(request):
    """Register a player and send them to the correct room"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            player_name = form.cleaned_data['player_name']
            room_name = form.cleaned_data['room_name']
            user_list.add_user(player_name)
            logger.debug(f"{player_name} is joining the game")
            client.set('user_list', pickle.dumps(user_list))
            return HttpResponseRedirect(f"/{room_name}/{player_name}/")

def unregister_user(request):
    if request.method == 'POST':
        player_data = json.loads(request.body)
        user_list.remove_user(player_data)
        client.set('user_list', pickle.dumps(user_list))
        logger.debug(f'{player_data["player"]} has left the game' )
        return HttpResponseRedirect('/')
    else:
        return HttpResponseNotAllowed(['POST'])
        

def get_user_table(request):
    if request.method == 'GET':
        table_data = pickle.loads(client.get('user_list'))
        json_data = json.dumps(table_data.get_connected_users())
        logger.debug(json_data)
        return JsonResponse(json_data, safe=False)

def validate_answer(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        choice = Choices.objects.get(question_id_id=data['question_id'])
        return JsonResponse({"answer": choice.check_correct_answer(data['answer'])})

def generate_game(request):
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            player_name = form.cleaned_data['player_name']
            room_name = form.cleaned_data['room_name']
            num_questions = form.cleaned_data['question_count']
            user_list.add_user(player_name)
            logger.debug(f"{player_name} is joining the game")
            client.set('user_list', pickle.dumps(user_list))
            logger.debug(f"Number of Questions {num_questions}")
            client.set("num_questions", num_questions)
            room_list.append(room_name)
            __encode_pickle("games",room_list)

            return HttpResponseRedirect(f"/{room_name}/{player_name}/")

def get_remaining_questions(request):
    num_questions = client.get("num_questions")
    return JsonResponse({'remaining_questions': int(num_questions)})


def __decode_pickle(key):
    return pickle.loads(client.get(key))

def __encode_pickle(key, data):
    encoded = pickle.dumps(data)
    client.set(key, encoded)