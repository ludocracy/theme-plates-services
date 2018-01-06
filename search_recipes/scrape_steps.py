from scrapely import Scraper
s = Scraper()
# assumes event member 'url' with value of url to be scraped for recipe steps
# TODO make this its own lambda later!!
def lambda_handler(event, context):
    url = event['url']
    steps = []
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
    return steps
