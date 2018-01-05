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

# takes json fro edamam api and returns in open-recipe-format
def format_open_recipe(edamam_json):
    src_json = edamam['recipe']
    recipe_json = {}
    recipe_json['recipe_name'] = src_json['label']
    recipe_json['source_url'] = src_json['url']
    recipe_json['yields'] = {
        'amount': src_json['yield'],
        'unit': 'servings'
    }

    recipe_json['ingredients'] = map(extract_ingredients, src_json['ingredients'])
    recipe_json['recipe_name'] = src_json['']
    recipe_json['recipe_name'] = src_json['']
    recipe_json['recipe_name'] = src_json['']
    return recipe_json

def extract_ingredients(ingredient_json):


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
