from types import SimpleNamespace
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from search_recipes.search_recipes import lambda_handler
from search_recipes.scrape_steps import lambda_handler as scrape_steps

def test_searchRecipes():
    queryStringParameters = {
        'q': 'potato pie'
    }

    res = lambda_handler(SimpleNamespace(**{
        'queryStringParameters': queryStringParameters,
        'httpMethod': 'GET'
    }), {})

    print(res)

def test_scrape_steps():
    url = "http://allrecipes.com/recipe/217899/mozzarella-stuffed-pesto-turkey-meatballs/?src=VD_Summary"
    res = scrape_steps({ 'url': url }, {})
    print(res[0])
    print(len(res[0].keys()))

# test_searchRecipes()
test_scrape_steps()
