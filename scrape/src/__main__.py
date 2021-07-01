
from urllib.robotparser import RobotFileParser
import time
from datetime import datetime
import numpy as np
from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver import (
  ChromeOptions,
  FirefoxOptions,
)
from \
  selenium.webdriver.remote \
  .webdriver \
import (
  WebDriver,
)
import re

from \
  selenium.webdriver \
  .common.by \
import (
  By,
)


def create_driver(
) -> WebDriver:
  options = FirefoxOptions()
  options.headless = True
  # options.add_argument('--no-sandbox')


  driver = webdriver.Firefox(
    options=options,
  )
  return driver



from \
  lib.pixiv.scrape \
  .ranked_free_comic \
import (
  # ScrapeFreeComic,
  # FreeComic,
  ScrapeRankedFreeComics,
)

import dataclasses
import typing

import requests
import bs4 


  
def main():
  site_url ="https://comic.pixiv.net/"

  driver = create_driver()

  scrape = (
    ScrapeRankedFreeComics()
  )
  for comic in scrape(driver):
    print(comic)
    print()
    # break 
  
  driver.close()

 

if __name__ == '__main__':
  main()


'''TODO
url -> anime_id
author -> author_text
follower -> follower_cnt
rank
ranked_field
update -> latest_update

''' 
