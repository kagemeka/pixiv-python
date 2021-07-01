
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
  lib.pixiv.scrape.free_comic \
import (
  ScrapeFreeComic,
)

import dataclasses
import typing

import requests
import bs4 


  
def main():
  site_url ="https://comic.pixiv.net/"
  comic_ranking = []
  # follower_count = []

  # driver = create_driver()
          
  # tg_url = site_url + "rankings"




  # driver.get(tg_url)
  
  # driver.close()

  scrape = ScrapeFreeComic()

  id_ = 7557
  res = scrape(id_)
  print(res)
 

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
