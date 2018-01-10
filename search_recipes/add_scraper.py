import sys
import json
import re
from io import StringIO
from scrapely import Scraper

def open_training_file():
    with open(sys.argv[1]) as training_params_file:
        return json.load(training_params_file)

def open_scrapers_file(url):
    with open('scrapers.json', 'r') as scrapers_file:
        domain = re.search(r'(?<=\/\/)[\w\.-]+(?=\/)', url).group()
        scrapers_json = json.load(scrapers_file)
        io = StringIO('')
        scraper.tofile(io)
        scrapers_json[domain] = json.loads(io.getvalue())
        return scrapers_json

# TODO add help and verbose modes
# TODO add arg validation and error feedback
scraper = Scraper()
url = sys.argv[2]
training_params = None
training_params = open_training_file()
assert training_params, "no training parameters found in {}".format(sys.argv[1])
scraper.train(url, training_params)
# TODO replace this with database action and maybe do checksum compare to avoid writing same scraper more than once?
scrapers_json = open_scrapers_file(url)

with open('scrapers.json', 'w') as scrapers_file:
    json.dump(scrapers_json, scrapers_file)
