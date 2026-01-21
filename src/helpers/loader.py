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
                interval_minutes = data.get("interval-minutes"),
                timeout_seconds = data.get("timeout-seconds"),
                retries = data.get("retries"),
            )
            raw_websites = data.get("websites", [])
            normalized_websites = []
            for raw in raw_websites:
                normalized_obj = normalize_url(raw)
                normalized_websites.append(normalized_obj)
    except FileNotFoundError:
        logger.warning(f"Configuration file {config} not found.", exc_info=e)
    
    return normalized_websites, config
