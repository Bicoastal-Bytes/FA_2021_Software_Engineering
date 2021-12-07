from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here:
class Category(models.Model):
    """Model representing the category that a Question is part of"""
    name = models.CharField("Category Name", max_length=60)

    def __str__(self):
        return self.name

class Question(models.Model):
    """Model representing a Question stored in the database"""
    category = models.ForeignKey(Category, on_delete=CASCADE)
    question = models.CharField("Question", max_length=1000)
    point_value = models.IntegerField("Question Point Value")

    def __str__(self):
        return self.question

    def question_point_value(self):
        return self.point_value
class Choices(models.Model):
    """Model representing the choices that a user has for questions"""
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    choices = models.JSONField("Choices")
    correct_answer = models.CharField("Correct Answer", max_length=300)

    def check_correct_answer(self, answer):
        return True if answer == self.correct_answer else False


