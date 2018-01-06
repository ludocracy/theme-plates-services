from types import SimpleNamespace
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from search_recipes.search_recipes import lambda_handler

def test_searchRecipes():
    queryStringParameters = {
        'q': 'potato pie'
    }

    result = lambda_handler(SimpleNamespace(**{
        'queryStringParameters': queryStringParameters,
        'httpMethod': 'GET'
    }), {})

    print(result)

# def test_parse_ingredients:

test_searchRecipes()
