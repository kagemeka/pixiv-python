
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
  lib.pixiv.scrape.free_comic \
import (
  ScrapeFreeComic,
  FreeComic,
)

import dataclasses
import typing

import requests
import bs4 



@dataclasses.dataclass
class RankedFreeComic(
  FreeComic,
):
  category: str
  rank: int


class ScrapeRankedFreeComic():
  
  def __call__(
    self,
    category: str,
    section: bs4.element.Tag,
  ) -> RankedFreeComic:
    self.__category = category
    self.__section = section
    self.__scrape()
    return self.__comic
  

  def __get_rank(
    self,
  ) -> typing.NoReturn:
    elm = self.__section
    elm = elm.find_element(
      by=By.CLASS_NAME,
      value='jsx-905610923',
    )
    self.__rank = int(elm.text)
  

  def __get_comic_id(
    self,
  ) -> typing.NoReturn:
    elm = self.__section
    url = elm.get_attribute(
      'href',
    )
    self.__comic_id = int(
      url.split('/')[-1],
    )
  

  def __scrape(
    self,
  ) -> typing.NoReturn:
    self.__get_rank()
    self.__get_comic_id()
    comic = ScrapeFreeComic()(
      self.__comic_id,
    )
    comic = RankedFreeComic(
      comic.comic_id,
      comic.metadata,
      comic.summary,
      comic.tags,
      comic.episode,
      self.__category,
      self.__rank,
    )
    self.__comic = comic
      



from typing import (
  List,
)

class ScrapeRankedFreeComics():
  
  def __call__(
    self,
    driver: WebDriver,
  ) -> typing.Iterator[
    RankedFreeComic
  ]:
    self.__driver = driver
    return self.__scrape()


  def __find_categories(
    self,
  ) -> typing.NoReturn:
    driver = self.__driver
    driver.get(self.__url)
    ls = driver.find_elements(
      by=By.CLASS_NAME,
      value=(
        'Menues_menu__p0ouK'
      ),
    )
    self.__categories = ls
  

  def __get_sections(
    self,
  ) -> typing.Iterator[
    bs4.element.Tag
  ]:
    driver = self.__driver
    ls = driver.find_element(
      by=By.CLASS_NAME,
      value=(
        'OfficialWorks_container__eNKQ2'
      ),
    ).find_elements(
      by=By.CLASS_NAME,
      value='OfficialWorkListItem_ranked__2ydPC',
    )
    for section in ls:
      yield section

  

  def __init__(
    self,
  ) -> typing.NoReturn:
    self.__url = (
      'https://comic.pixiv.net'
      '/rankings'
    )



  def __scrape(
    self,
  ) -> typing.Iterator[
    RankedFreeComic
  ]:
    self.__find_categories()
    f = ScrapeRankedFreeComic()
    categs = self.__categories
    for category in categs:
      category.click()
      s = self.__get_sections()
      for section in s:
        yield f(
          category.text,
          section,
        )


  
def main():
  site_url ="https://comic.pixiv.net/"

  driver = create_driver()
          
  tg_url = site_url + "rankings"



  
  driver.get(tg_url)

  scrape = (
    ScrapeRankedFreeComics()
  )
  for comic in scrape(driver):
    print(comic)
    print()
    # break 
  
  driver.close()

  # scrape = ScrapeFreeComic()

  # id_ = 7557
  # res = scrape(id_)
  # print(res)
 

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
