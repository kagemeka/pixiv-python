
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



import dataclasses
import typing


@dataclasses.dataclass
class Episode:
  latest_update: datetime
  oldest_update: datetime
  count: int


@dataclasses.dataclass
class Metadata:
  title: str
  author_text: str
  magazine: str


import bs4 
class ScrapeMetadata():
  
  def __call__(
    self,
    soup: bs4.BeautifulSoup,
  ) -> Metadata:
    self.__soup = soup
    self.__scrape()
    print(self.__meta)
    return self.__meta

    
  def __get_txt(
    self,
    cls_: str,
  ) -> str:
    return self.__soup.find(
      class_=cls_,
    ).text 


  def __scrape(
    self,
  ) -> typing.NoReturn:
    classes = (
      'jsx-2099034544',
      'jsx-173046405',
      'jsx-2154117046',
    )
    self.__meta = Metadata(
      *(
        self.__get_txt(cls_)
        for cls_ in classes
      ),
    )



import requests
import bs4 

@dataclasses.dataclass
class FreeComic():
  ...




class ScrapeFreeComic():
  ...

  def __call__(
    self,
    comic_id: int,
  ) -> FreeComic:
    self.__id = comic_id
    self.__make_soup()
    self.__scrape()
    

  
  def __init__(
    self,
  ) -> typing.NoReturn:
    self.__base_url = (
      'https://comic.pixiv.net'
      '/works/'
    )


  def __make_soup(
    self,
  ) -> typing.NoReturn:
    base_url = self.__base_url
    id_ = self.__id
    response = requests.get(
      f'{base_url}/{id_}',
    )
    soup = bs4.BeautifulSoup(
      response.content,
      'html.parser',
    )
    self.__soup = soup


  
  def __scrape(
    self,
  ) -> typing.NoReturn:
    meta = ScrapeMetadata()
    meta(self.__soup)


  
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
  scrape(id_)
 

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
