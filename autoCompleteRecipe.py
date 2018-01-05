# assumes event has body in open-recipe-format JSON
def lambda_handler(event, context):
    recipe = event.body
    # TODO iterate through possible fields and check value
    # TODO if required and invalid, add "incomplete" flag to recipe
    # TODO add missing fields by:
    #   - identifying domain
    #   - calling up appropriate scrapely object
    return recipe
