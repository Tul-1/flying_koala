from django.contrib import admin
from .models import Recipe, Ingredient, Quantity, UserRecipeData

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Quantity)
admin.site.register(UserRecipeData)
