
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



@dataclasses.dataclass
class Summary():
  overview: str
  follower_cnt: int
  genres: typing.List[str]



class ScrapeSummary():

  def __call__(
    self,
    soup: bs4.BeautifulSoup,
  ) -> Summary:
    self.__soup = soup
    self.__scrape()
    return Summary(
      self.__overview,
      self.__follower_cnt,
      self.__genres,
    )


  def __get_overview(
    self,
  ) -> typing.NoReturn:
    elm = self.__soup.find(
      class_='jsx-3803037064',
    )
    self.__overview = elm.text
  

  def __get_follower_cnt(
    self,
  ) -> typing.NoReturn:
    elm = self.__soup.find(
      class_='jsx-736239241',
    )
    self.__follower_cnt = int(
      elm.text.replace(
        ',', 
        '',
      ),
    )
  
  def __get_genres(
    self,
  ) -> typing.NoReturn:
    ls = self.__soup.find(
      class_='Introduce_categories__kSPxI',
    ).find_all(
      class_='jsx-1140918973',
    )
    self.__genres = [
      elm.text
      for elm in ls
    ]


  def __scrape(
    self,
  ) -> typing.NoReturn:
    self.__get_overview()
    self.__get_follower_cnt()
    self.__get_genres()


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
    summary = ScrapeSummary()
    s = summary(self.__soup)
    print(s)


  
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
