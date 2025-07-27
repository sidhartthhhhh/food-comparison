from django.test import TestCase


from django.urls import path
from .views import search_food_items

urlpatterns = [
    path('search/', search_food_items, name='food-item-search'),
]