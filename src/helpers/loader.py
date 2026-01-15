import json
from .normalize_url import normalize_url
from .logger import logger
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
        logger.error(f"Configuration file {config} not found.", exc_info=e)
        with open("./logs/monitor.log", 'w') as config_file:
            config_file.write("")
    return normalized_websites, config
