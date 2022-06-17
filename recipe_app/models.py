from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    serves = models.IntegerField(default=1)
    prep_time = models.IntegerField(default=1)
    cuisine = models.CharField(max_length=50, default="None set")

    steps = models.TextField(max_length=10000)

    pub_date = models.DateTimeField('date published')
    username = models.CharField(max_length=200)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    like_number = models.IntegerField(default=0)
    user_likes = models.ManyToManyField(User, related_name='user_likes')

    def __str__(self):
        return self.recipe_name

class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=100)
    recipe = models.ManyToManyField(Recipe, through="Quantity")

    def __str__(self):
        return self.ingredient_name

class Quantity(models.Model):
    quantity = models.CharField(max_length=50)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quantity} - {self.recipe.recipe_name} - {self.ingredient.ingredient_name}'

class UserRecipeData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.amount)

