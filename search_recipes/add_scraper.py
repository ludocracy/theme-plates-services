import sys
import json
from scrapely import Scraper

# TODO add help and verbose modes
# TODO add arg validation and error feedback
scraper = Scraper()
url = sys.argv[2]
training_params = None
with open(sys.argv[1]) as training_params_file:
    training_params = json.load(training_params_file)
assert training_params, "no training parameters found in {}".format(sys.argv[1])
scraper.train(url, training_params)
domain = re.search(r'(?<=\/\/).+(?=\/)', url).group()
# TODO replace this with database action and maybe do checksum compare to avoid writing same scraper more than once?
with open('scrapers.json') as scrapers_file:
    scrapers_json = json.load(scrapers_file)
    scrapers_json[domain] = scraper
    json.dump(scrapers_json, scrapers_file)
