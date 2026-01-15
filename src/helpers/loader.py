import json
from .normalize_url import normalize_url
from ..services import model

config_path = "./config.json"

def loader():
    try:
        with open(config_path, 'r') as readFile:
            data = json.load(readFile)
            config = model.Config(
                interval_minutes = data.get("interval_minutes", 30),
                timeout_seconds = data.get("timeout_seconds", 5),
                retries = data.get("retries", 3),
            )
            raw_websites = data.get("websites", [])
            normalized_websites = []
            for raw in raw_websites:
                normalized_obj = normalize_url(raw)
                normalized_websites.append(normalized_obj)
    except FileNotFoundError:
        print("file not found!")
    return normalized_websites, config
