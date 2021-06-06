""" Prepare Recipes for the model_bakery  test model instances """
from itertools import cycle
from model_bakery.recipe import Recipe, foreign_key
from performances.models import (
    Class, Performance,
    Theater, Event, Institution, Locality)

performance_class = Recipe(
    Class,
    performance_duration=5)

zone_names = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
region_names = ['Makueni', 'Uasin Gishu', 'Garissa']
locality = Recipe(
    Locality,
    zone=cycle(zone_names),
    county=cycle(region_names)
)

institution_names = ['A', 'B', 'C', 'D', 'E']
institution = Recipe(
    Institution,
    name=cycle(institution_names),
    locality=foreign_key(locality))

venue = Recipe(
    Institution,
    name='Ngaa Primary School',
    locality=foreign_key(locality))
event = Recipe(
    Event,
    venue=foreign_key(venue),
    event_level='County')

performance = Recipe(
    Performance,
)
theater_names = ['Chapel', 'Mandela\'s Hall', 'Auditorium A', ]
theater = Recipe(
    Theater,
    name=cycle(theater_names),
    venue=foreign_key(event)
)
