from django.core.management.base import BaseCommand
from api.models import Question, Choices, Category
from os import listdir
from json import load
import random 

class Command(BaseCommand):
    help = 'Imports data into the database'

    def handle(self, *args, **kwargs):
        '''Function overloaded to work with Django's manage.py'''
        # Set base dir
        dir = 'api/db_json/'
        # Get all of the files in directory
        files = listdir(dir)
        # Categories for the Database
        categories = [
            "Entertainment: Books",
            "Animals",
            "Celebrities",
            "Science: Computers",
            "Entertainment: Film",
            "Geography",
            "History",
            "Science: Mathematics"
        ]
        # Create categories in database
        for category in categories:
            cat = Category.objects.create(name=category)
        # Add questions and choices to database
        for file in files:
            with open(dir + file, 'r') as json_file:
                # Load the data from the file as JSON data
                json_data = load(json_file)
                # Get data from the results   
                for entry in json_data['results']:
                    point_value = 0
                    # Checking for difficulty and then setting values based on that 
                    if entry['difficulty'] == 'easy':
                        point_value = random.randrange(100, 201, 100)
                    if entry['difficulty'] == 'medium':
                        point_value = random.randrange(300, 401, 100)
                    if entry['difficulty'] == 'hard':
                        point_value = random.randrange(500, 601, 100)
                    # Getting the category object
                    cat = Category.objects.filter(name=entry['category'])
                    # Create a question object
                    q = Question.objects.create(category=cat[0], question=entry['question'], point_value=point_value)
                    # Create a choice object
                    c = Choices.objects.create(question_id=q, choices=entry['choices'], correct_answer=entry['correct_answer'] )
