# assumes event has body in open-recipe-format JSON
def lambda_handler(event, context):
    recipe = event.body
    # TODO iterate through possible fields and check value
    # TODO if required and invalid, add "incomplete" flag to recipe
    # TODO add missing fields by:
    #   - identifying domain
    #   - calling up appropriate scrapely object from file (in db)
    # if scrapely fails:
    #  1. check if saved scraper fails on training site
    #  2. if training site also fails, retrain and save new scraper
    # retry scrape.
    # if retry fails, return empty object.
    return recipe
