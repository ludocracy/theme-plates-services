def lambda_handler(event, context):
    return {
        'GET': get_recipes(event.queryStringParameters)
    }[event.httpMethod] or {}

def get_recipes(params):
    # TODO maybe do some NLP clean up and tagging of search terms here
    query = params['q']
    # TODO use pagination and default list size!
    results = edamam_api(query)
    # TODO filter search results by various params
    # TODO sort by various params criteria
    recipes = map(get_recipe, results)
    return recipes

def get_recipe(edamam_json):
    # TODO hit edamam api and set results to list
    # TODO use env vars for edamam api
    return recipe_json

def complete_recipe(open_recipe)
