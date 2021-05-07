""" Prepare Recipes for the model_bakery  test model instances """
from itertools import cycle
from model_bakery.recipe import Recipe, foreign_key
from performances.models import (
    Class, Performance,
    Theater, Event)


performance_class = Recipe(
    Class,
    performance_duration=5)

event = Recipe(
    Event, venue="Bomas of Kenya")

theater_names = ['Chapel', 'Mandela\'s Hall', 'Auditorium A', ]
theater = Recipe(
    Theater,
    name=cycle(theater_names),
    venue=foreign_key(event)
)





