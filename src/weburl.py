import json
from urllib.parse import urlparse
config = "./config.json"

def web_url():
    with open(config, 'r') as readFile:
        config_data = json.load(readFile)

        interval = config_data.get("interval_minutes", 30)
        timeout = config_data.get("timeout_seconds", 5)
        websites = config_data.get("websites", [])

    schemes = ['http://', 'https://']
    for website in websites:
        original_url = website
        print(original_url)
        if website.startswith('http://', 0) or website.startswith('https://', 0) and website.endswith('/', -1):
            website_domain = website.split('//')[1].split('/')[0]
        elif website.startswith('http://', 0) or website.startswith('https://', 0):
            website_domain = website.split('//')[1]
        if '/' in website_domain:
            website_domain = website_domain.split('/')[0]
        elif website.startswith('www.', 0) and website.endswith('/', -1):
            website_domain = website.split('www.')[1].split('/')[0]
        elif website.endswith('/', -1):
            website_domain = website[:-1]
        elif ':' in website:
            website_domain = website.split(':')[0]
        else:
            website_domain = website
        
        print("full url", original_url, "domain", website_domain)
    return original_url, website_domain, interval, timeout
web_url()