import os
import urllib.parse
import urllib.request
import json

from .ingredients import extract_ingredient_data
from .scrape_steps import lambda_handler as scrape_steps

# hits edamam api for results
# TODO consider having it hit our cache for search results and doing a map reduce
# TODO in this case, the below method becomes generic and we pass an array of services to call
def get_recipes(params):
    # TODO maybe do some NLP clean up and tagging of search terms here
    results = search_edamam(params)
    # TODO filter search results by various params
    # TODO sort by various params criteria
    recipes = map(format_open_recipe, results)
    return list(recipes)

def search_edamam(query_params):
    default_query_params = {
        'app_id': os.environ['edamam_id'],
        'app_key': os.environ['edamam_key'],
        'from': 0,
        'to': 1
    }
    final_query_params = {**default_query_params, **query_params}
    params = urllib.parse.urlencode(final_query_params)
    url = os.environ['edamam_url'] + params
    response = urllib.request.urlopen(url).read()
    return json.loads(response)['hits']

# takes json from edamam api and returns in open-recipe-format
def format_open_recipe(edamam_json):
    src_json = edamam_json['recipe']
    # TODO pull from cache if it exists
    ingredients = list(map(extract_ingredient_data, src_json['ingredients']))
    return {
        'recipe_name': src_json['label'],
        'source_url': src_json['url'],
        'yields': {
            'amount': src_json['yield'],
            'unit': 'servings'
        },
        'ingredients': ingredients,
        'steps': scrape_steps({'url': src_json['url']}, {})
    }
