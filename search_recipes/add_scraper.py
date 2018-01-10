import sys
import json
import re
from io import StringIO
from scrapely import Scraper

def open_training_file():
    file_name = sys.argv[1] if len(sys.argv) > 1 else "training_file.json"
    with open(file_name) as training_params_file:
        return json.load(training_params_file)

def update_scrapers_file(url):
    domain = re.search(r'(?<=\/\/)[\w\.-]+(?=\/)', url).group()
    scraper_file_name = ""
    scrapers_json = {}
    with open('scrapers.json', 'r') as scrapers_file:
        scrapers_json = json.load(scrapers_file)

    scraper_file_name = domain + ".json"
    scrapers_json[domain] = scraper_file_name
    with open('scrapers.json', 'w') as scrapers_file:
        json.dump(scrapers_json, scrapers_file)

    return scraper_file_name

# TODO add help and verbose modes
# TODO add arg validation and error feedback
scraper = Scraper()
training_params = open_training_file()
assert training_params, "no training parameters found in {}".format(sys.argv[1])
url = training_params['url']
params = training_params['params']
scraper.train(url, params)
# TODO replace this with database action and maybe do checksum compare to avoid writing same scraper more than once?
scraper_file_name = update_scrapers_file(url)

with open(scraper_file_name, 'w') as scraper_file:
    scraper.tofile(scraper_file)
