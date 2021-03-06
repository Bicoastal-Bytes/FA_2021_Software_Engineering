from warnings import catch_warnings
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
import base64

logger = logging.getLogger(__name__)

client = redis.client.StrictRedis()

user_list = UserTracker()

room_list = []

category_list = []

# Create your views here.

def get_question(request):
    """Get a question from a specific category and point value"""
    if request.method == 'GET':
        category = request.GET['category']
        points = request.GET['points']
        question = list(Question.objects.filter(category__name=category, point_value=points))
        logger.debug(f"Communicating with database to get question: {question[0]}")
        choices = list(Choices.objects.filter(question_id=question[0].id))
        logger.debug(f"Communicating with database to get choices for question: {choices[0].id}")

        random.shuffle(choices[0].choices)
        response_data = {
            "question": question[0].question,
            "question_id": question[0].id,
            "choices": choices[0].choices,
            "choices_id": choices[0].id,
            "correct_answer": str(base64.b64encode(choices[0].correct_answer.encode('utf-8')), "utf-8")
        }
        logger.debug('Sending data back to client')
        remaining_questions = int(client.get("num_questions"))
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
        user_list.remove_user(player_data['player'])
        client.set('user_list', pickle.dumps(user_list))
        logger.debug(f'{player_data["player"]} has left the game' )
        return HttpResponseRedirect('/')
    else:
        return HttpResponseNotAllowed(['POST'])
        

def get_user_table(request):
    if request.method == 'GET':
        table_data = pickle.loads(client.get('user_list'))
        # json_data = json.dumps(table_data.get_connected_users())
        json_data = json.dumps(user_list.get_connected_users())
        logger.debug(json_data)
        return JsonResponse(json_data, safe=False)

def validate_answer(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        logger.debug(f"Data recieved: {data}")
        choice = Choices.objects.get(question_id_id=data['question_id'])
        question = Question.objects.get(id=data['question_id'])
        points = question.question_point_value()
        current_player = user_list.get_active_player()
        result = choice.check_correct_answer(data['answer'])
        logger.debug(f'''Question point value {points}''')
        if result:
            user_list.set_player_score(current_player, points/10)
        else:
            user_list.set_player_score(current_player, -points/10)
        
        return JsonResponse({"answer": result})

def generate_game(request):
    if request.method == 'POST':
        form = CreationForm(request.POST)
        if form.is_valid():
            player_name = form.cleaned_data['player_name']
            room_name = form.cleaned_data['room_name']
            num_questions = form.cleaned_data['question_count']
            user_list.add_user(player_name)
            user_list.make_player_active(player_name)
            logger.debug(f"{player_name} is joining the game")
            client.set('user_list', pickle.dumps(user_list))
            logger.debug(f"Number of Questions {num_questions}")
            client.set("num_questions", num_questions)
            room_list.append(room_name)
            __encode_pickle("games",room_list)
            logger.debug('Recieved a GET request for a category')
            categories = list(Category.objects.all())
            logger.debug('Getting all categories from database')
            random_cats = random.sample(categories, 6)
            category_list.extend(random_cats)
            logger.debug(category_list)
            logger.debug('Choosing a random category')
            return HttpResponseRedirect(f"/{room_name}/{player_name}/")

def get_remaining_questions(request):
    num_questions = client.get("num_questions")
    return JsonResponse({'remaining_questions': int(num_questions)})

def get_active_player(request):
    player_name = user_list.get_active_player()
    logger.debug('Active Player Name' + player_name)
    return JsonResponse({'player': player_name})

def get_category(request):
    """Get a random category when called"""
    if request.method == "GET":
        random_category = random.choice(category_list)
        id = category_list.index(random_category)
        if id == 0:
            id = 30
        elif id == 1:
            id = 90
        elif id == 2:
            id = 150
        elif id == 3:
            id = 210
        elif id == 4:
            id = 270
        else:
            id = 330
        response_data = {
           'category': random_category.name,
           'id': id 
        }
        return JsonResponse(response_data)
    else:
        return HttpResponseNotAllowed(['GET'])

def populate_wheel(request):
    if request.method == "GET":
        categories = []
        i = 1
        for cat in category_list:
            data = {
                'name': cat.name,
                'id': i * 30
            }
            i += 2
            categories.append(data)
        return_value = {
            "categories": categories
        }
        return JsonResponse(return_value)

def buzz_in(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        logger.debug(f"Data recieved: {data}")
        current_player = user_list.get_active_player()
        logger.debug(current_player)
        if current_player != data['player']:
            user_list.make_player_inactive(current_player)
            user_list.make_player_active(data['player'])
            logging.debug(user_list.get_active_player())
        return JsonResponse({'active_player': user_list.get_active_player()})


def __decode_pickle(key):
    return pickle.loads(client.get(key))

def __encode_pickle(key, data):
    encoded = pickle.dumps(data)
    client.set(key, encoded)

