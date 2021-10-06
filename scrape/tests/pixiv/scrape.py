import typing
import sys 
import time
from selenium.webdriver import (
  Chrome,
  ChromeOptions,
  Firefox,
  FirefoxOptions,
)
from selenium.webdriver.remote.webdriver import WebDriver

def create_driver() -> WebDriver:
  options = FirefoxOptions()
  options.headless = True
  return Firefox(options=options)




def set_globals() -> typing.NoReturn:
  import os 
  global cfd, root 
  cfd = os.path.abspath(os.path.dirname(__file__))
  root = os.path.abspath(f'{cfd}/../..')


set_globals()
sys.path.append(f'{root}/src')

from lib.pixiv.scrape import scrape_free_ranking
from lib.pixiv.scrape import scrape_free_comic


def test_scrape_free_ranking() -> typing.NoReturn:
  driver = create_driver()
  ranking = scrape_free_ranking(driver)
  driver.close()
  print(ranking)


def test_scrape_free_comic() -> typing.NoReturn:
  comic_id = 7800
  comic = scrape_free_comic(comic_id)
  print(comic)


if __name__ == '__main__':
  test_scrape_free_ranking()
  # test_scrape_free_comic()