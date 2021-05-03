""" Prepare Recipes for the model_bakery  test model instances """
from itertools import cycle
from model_bakery.recipe import Recipe
from performances.models import Class, Performance


performance_class = Recipe(
    Class,
    performance_duration=5
)



