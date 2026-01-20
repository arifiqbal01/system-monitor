
from src.helpers.logger import logger
from json import dumps, loads
from src.services.model import Website, CheckResult, WebStatus, WebsiteReport

def summary_maker(reports):
  up_websites = []
  down_websites = []
  degraded_websites = []
  unkown_websites = []
  web_count = 0
  up_count = 0
  down_count = 0
  degraded_count = 0
  unknown_count = 0
 
  for report in reports:
    web_count += 1
    if report.status == "UP":
      up_count += 1
      up_websites.append(report.website)
    elif report.status == "DOWN":
      down_count += 1
      down_websites.append(report.website)
    elif report.status == "DEGRADED":
      degraded_count += 1
      degraded_websites.append(report.website)
    elif report.status == "UNKNOWN":
      unknown_count += 1
      unkown_websites.append(report.website)

  print(f"total websites = {web_count}, up = {up_count}: {up_websites}, down = {down_count}: {down_websites}, degraded = {degraded_count}: {degraded_websites}, unknown = {unknown_count}: {unkown_websites}")

  return