from .recipe import get_recipes

def lambda_handler(event, context):
    return {
        'GET': get_recipes(event.queryStringParameters)
    }[event.httpMethod] or {}
