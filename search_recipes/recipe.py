import os
import urllib.parse
import urllib.request
import json
from yaml import load  # TODO remove when we switch to DB!

from .ingredients import extract_ingredient_data
from .scrape_steps import lambda_handler as scrape_steps

# hits edamam api for results
# TODO consider having it hit our cache for search results and doing a map reduce
# TODO in this case, the below method becomes generic


def get_recipes(params: dict) -> list:
    # TODO maybe do some NLP clean up and tagging of search terms here
    results = search_edamam(params)
    # TODO don't forget that themePlates-defined search criteria will need to be handled here
    recipes = map(format_open_recipe, results)
    return list(recipes)  # TODO make this a set?


def search_edamam(query_params: dict) -> dict:
    configs = load_api_configs()
    default_query_params = {
        'app_id': configs['edamam_id'],
        'app_key': configs['edamam_key'],
        'from': 0,
        'to': 1
    }
    final_query_params = {**default_query_params, **query_params}
    query_param_str = urllib.parse.urlencode(final_query_params)
    base_url = configs['edamam_url']
    url = f'{base_url}?{query_param_str}'
    response = urllib.request.urlopen(url).read()
    return json.loads(response)['hits']


def load_api_configs() -> dict:
    config_file = 'search_recipes/.edamam.config.yaml'
    with open(config_file) as edamam_configs_file:
        return load(edamam_configs_file)

# takes json from edamam api and returns in open-recipe-format


def format_open_recipe(edamam_dict: dict) -> dict:
    src_dict = edamam_dict['recipe']
    # TODO pull from cache if it exists
    ingredients = list(map(extract_ingredient_data, src_dict['ingredients']))
    return {
        'recipe_name': src_dict['label'],
        'source_url': src_dict['url'],
        'yields': {
            'amount': src_dict['yield'],
            'unit': 'servings'
        },
        'ingredients': ingredients,
        'steps': scrape_steps({'url': src_dict['url']}, {})
    }
