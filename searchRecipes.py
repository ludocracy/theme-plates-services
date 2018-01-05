import json
import urllib.request
import urllib.parse
import os

# for DEV purposes only
from types import SimpleNamespace
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def lambda_handler(event, context):
    return {
        'GET': get_recipes(event.queryStringParameters)
    }[event.httpMethod] or {}

# hits edamam api for results
# TODO consider having it hit our cache for search results and doing a map reduce
def get_recipes(params):
    # TODO maybe do some NLP clean up and tagging of search terms here
    query = params['q']
    # TODO use pagination and default list size!
    results = edamam_api(query)
    # TODO filter search results by various params
    # TODO sort by various params criteria
    recipes = map(format_open_recipe, results)
    return list(recipes)

def edamam_api(query):
    params = urllib.parse.urlencode({
        'q': query,
        'app_id': os.environ['edamam_id'],
        'app_key': os.environ['edamam_key'],
        'from': 0,
        'to': 10
    })
    url = os.environ['edamam_url'] + params
    response = urllib.request.urlopen(url).read()
    return json.loads(response)['hits']

# takes json from edamam api and returns in open-recipe-format
def format_open_recipe(edamam_json):
    src_json = edamam_json['recipe']
    ingredients = list(map(extract_ingredients, src_json['ingredients']))
    return {
        'recipe_name': src_json['label'],
        'source_url': src_json['url'],
        'yields': {
            'amount': src_json['yield'],
            'unit': 'servings'
        },
        'ingredients': ingredients,
        # 'steps': TODO call scrapely
    }

def extract_ingredients(ingredient_json):
    from functools import reduce

    word_list = [[]] + ingredient_json['text'].split(' ')
    amount, unit, name = reduce(parse_ingredient_str, word_list)
    print(amount)
    print(unit)
    print(name)
    print(type(name))
    return {
        'name': {
            'amount': amount,
            'unit': unit,
            # 'processing': processing
        }
    }

def parse_ingredient_str(lyst, str):
    if len(lyst) < 3:
        lyst.append(str)
    else:
        lyst[2] += str + ' '
    return lyst

def test_searchRecipes():
    queryStringParameters = {
        'q': 'potato pie'
    }

    result = lambda_handler(SimpleNamespace(**{
        'queryStringParameters': queryStringParameters,
        'httpMethod': 'GET'
    }), {})

    print(result)

test_searchRecipes()
