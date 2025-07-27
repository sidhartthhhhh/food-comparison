# api/views.py

import json
import os
from django.conf import settings
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

# --- Import these two new things ---
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

from rest_framework.response import Response

# api/views.py

def load_mock_data(platform_name):
    filename = f"{platform_name.lower()}_data.json"
    filepath = os.path.join(settings.BASE_DIR, 'mock_data', filename)

    try:
        # Add encoding="utf-8" here
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Mock data file not found at {filepath}")
        return []

# --- Add this new line right above your function ---
@renderer_classes([JSONRenderer])
@api_view(['GET'])
def search_food_items(request):
    """
    This API endpoint searches for a food item across Zomato and Swiggy,
    then combines the results into a single response.
    """
    search_term = request.query_params.get('search', '').lower()
    print(f"Received search request for: '{search_term}'")

    zomato_items = load_mock_data('zomato')
    swiggy_items = load_mock_data('swiggy')

    combined_results = {}

    for item in swiggy_items:
        item_name = item.get('name')
        if item_name and (not search_term or search_term in item_name.lower()):
            if item_name not in combined_results:
                combined_results[item_name] = {
                    "item_name": item_name,
                    "platforms": []
                }
            
            combined_results[item_name]['platforms'].append({
                "platform": "Swiggy",
                "price": item.get('price'),
                "rating": item.get('rating'),
                "delivery_time": f"{item.get('delivery_time_mins')} mins",
                "discount": item.get('discount', 'No discount'),
                "restaurant": item.get('restaurant'),
                "order_url": f"https://www.swiggy.com/search?query={item_name.replace(' ', '+')}"
            })

    for item in zomato_items:
        item_name = item.get('title')
        if item_name and (not search_term or search_term in item_name.lower()):
            if item_name not in combined_results:
                combined_results[item_name] = {
                    "item_name": item_name,
                    "platforms": []
                }
            
            combined_results[item_name]['platforms'].append({
                "platform": "Zomato",
                "price": item.get('cost'),
                "rating": item.get('user_rating'),
                "delivery_time": item.get('eta'),
                "discount": item.get('offer', 'No offer'),
                "restaurant": item.get('eatery'),
                "order_url": f"https://www.zomato.com/search?q={item_name.replace(' ', '+')}"
            })
    
    final_list = list(combined_results.values())
    return Response(final_list)