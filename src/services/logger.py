import logging

logger = logging.getLogger(__name__)
logger.setLevel("INFO")
console_handler = logging.StreamHandler()
console_handler.setLevel("INFO")
file_handler = logging.FileHandler("logs/monitor.log", encoding="utf-8", mode="a")
file_handler.setLevel("INFO")

logger.addHandler(console_handler)
logger.addHandler(file_handler)
formater = logging.Formatter(
    "{asctime} | {levelname} | {message}",
    style="{",
    datefmt="%Y-%m-%d | %H:%M"
)
console_handler.setFormatter(formater)
file_handler.setFormatter(formater)