import os
import urllib.parse
import urllib.request
import json

from pint import UnitRegistry
from pint.errors import UndefinedUnitError, DimensionalityError
ureg = UnitRegistry()

def lambda_handler(event, context):
    return {
        'GET': get_recipes(event.queryStringParameters)
    }[event.httpMethod] or {}

# hits edamam api for results
# TODO consider having it hit our cache for search results and doing a map reduce
# TODO in this case, the below method becomes generic and we pass an array of services to call
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
    ingredients = list(map(extract_ingredient_data, src_json['ingredients']))
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

def extract_ingredient_data(ingredient_json):
    amount, unit, name = parse_ingredient_str(ingredient_json['text'])
    return {
        'name': {
            'amount': amount,
            'unit': unit,
            # 'processing': processing
        }
    }

# assumes ingredient_str has three or more words
# TODO optimize this method!!!!
def parse_ingredient_str(ingredient_str):
    word_list = ingredient_str.split(' ')
    unit_word_cnt = 2
    units = ' '.join(word_list[:unit_word_cnt])
    quantity = try_parse_units(units)
    if quantity == None:
        quantity = try_parse_units(word_list[0])
        unit_word_cnt = 1

    if quantity == None:
        return [1, 'each', ingredient_str]

    if type(quantity) == int or type(quantity) == float:
        return [quantity, 'each', ' '.join(word_list[1:])]

    name = ' '.join(word_list[unit_word_cnt:])
    return [quantity.magnitude, quantity.units.__str__(), name]

def try_parse_units(s):
    try:
        return ureg.parse_expression(s)
    except (UndefinedUnitError, DimensionalityError):
        return None

def test_searchRecipes():
    from types import SimpleNamespace
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())

    queryStringParameters = {
        'q': 'potato pie'
    }

    result = lambda_handler(SimpleNamespace(**{
        'queryStringParameters': queryStringParameters,
        'httpMethod': 'GET'
    }), {})

    print(result)

test_searchRecipes()
