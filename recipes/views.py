from django.shortcuts import render
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def index(request):
    recipes = []
    ingredients = request.GET.get('ingredients', '').strip()
    api_error = None
    
    if ingredients:
        try:
            api_key = settings.SPOONACULAR_API_KEY
            url = f'https://api.spoonacular.com/recipes/findByIngredients'
            params = {
                'apiKey': api_key,
                'ingredients': ingredients,
                'number': 5,
                'ranking': 1,
                'ignorePantry': True
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                try:
                    api_response = response.json()
                    if isinstance(api_response, dict) and 'results' in api_response:
                        recipes = api_response['results']
                    elif isinstance(api_response, list):
                        recipes = api_response
                    else:
                        recipes = []
                except Exception as e:
                    logger.error(f"Error processing API response: {str(e)}")
                    recipes = []
                    api_error = "Error processing API response"
            else:
                api_error = f"API Error: {response.status_code} - {response.text}"
                logger.error(api_error)
        except Exception as e:
            api_error = f"Error fetching recipes: {str(e)}"
            logger.error(api_error)
    
    return render(request, 'recipes/index.html', {
        'recipes': recipes,
        'ingredients': ingredients,
        'api_error': api_error
    })

def recipe_detail(request, recipe_id):
    recipe = None
    api_error = None
    
    try:
        api_key = settings.SPOONACULAR_API_KEY
        url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
        params = {
            'apiKey': api_key,
            'includeNutrition': True
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            recipe = response.json()
        else:
            api_error = f"API Error: {response.status_code} - {response.text}"
            logger.error(api_error)
    except Exception as e:
        api_error = f"Error fetching recipe details: {str(e)}"
        logger.error(api_error)
    
    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'api_error': api_error
    })
    recipes = []
    ingredients = ''
    api_error = None
    
    # Get ingredients from GET parameters
    if request.method == 'GET' and request.GET:
        ingredients = request.GET.get('ingredients', '').strip()
        if ingredients:
            try:
                # Call Spoonacular API
                api_key = settings.SPOONACULAR_API_KEY
                url = f'https://api.spoonacular.com/recipes/findByIngredients'
                params = {
                    'apiKey': api_key,
                    'ingredients': ingredients,
                    'number': 5,
                    'ranking': 1,
                    'ignorePantry': True
                }
                
                logger.info(f"Making API request to: {url} with params: {params}")
                response = requests.get(url, params=params)
                logger.info(f"API Response Status: {response.status_code}")
                logger.info(f"API Response Content: {response.text}")
                
                if response.status_code == 200:
                    try:
                        api_response = response.json()
                        if isinstance(api_response, dict) and 'results' in api_response:
                            recipes = api_response['results']
                        elif isinstance(api_response, list):
                            recipes = api_response
                        else:
                            recipes = []
                        logger.info(f"Successfully received {len(recipes)} recipes")
                    except Exception as e:
                        logger.error(f"Error processing API response: {str(e)}")
                        recipes = []
                        api_error = "Error processing API response"
                else:
                    api_error = f"API Error: {response.status_code} - {response.text}"
                    logger.error(api_error)
            except Exception as e:
                api_error = f"Error calling API: {str(e)}"
                logger.error(api_error)

    return render(request, 'recipes/index.html', {
        'ingredients': ingredients,
        'recipes': recipes,
        'api_error': api_error
    })
