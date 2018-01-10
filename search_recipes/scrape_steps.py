import re
import json
import io
from scrapely import Scraper

# assumes event member 'url' with value of url to be scraped for recipe steps
# TODO make this its own lambda later!!
def lambda_handler(event, context):
    scraper = get_scraper(event['url'])
    if not scraper:
        return []
    # TODO if failure rate goes up
    # if scrapely fails:
    #  1. check if saved scraper fails on training site
    #  2. if training site also fails, retrain and save new scraper
    # retry scrape.
    return scraper.scrape(url)

# TODO later this should pull from db, assuming we'll need hundreds of scrapers
def get_scraper(url):
    domain = re.search(r'(?<=\/\/)[\w\.-]+(?=\/)', url).group()
    scraper_json = {}
    with open('scrapers.json', 'r') as scrapers_file:
        scrapers_json = json.load(scrapers_file)
        if domain in scrapers_json:
            scraper_json = scrapers_json[domain]
        else:
            return None

    print(scraper_json)
    scraper_file = json.dump(scraper_json, io.StringIO(''))
    return Scraper.fromfile(scraper_file)
