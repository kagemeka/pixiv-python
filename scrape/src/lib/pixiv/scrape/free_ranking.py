from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import (
  WebDriver,
  WebElement,
)
import dataclasses
import typing
import datetime 
import tqdm 



@dataclasses.dataclass
class FreeRankedComic():
  comic_id: int
  field: str
  rank: int



@dataclasses.dataclass
class Ranking():
  datetime: datetime.datetime 
  comics: typing.List[FreeRankedComic]



def __scrape_free_ranked_comic(
  field: str,
  element: WebElement,
) -> FreeRankedComic:
  def get_rank() -> int:
    rank = element.find_element(
      by=By.CLASS_NAME,
      value='text-xs'
    ).text
    return int(rank)

  def get_comic_id() -> typing.NoReturn:
    url = element.get_attribute('href')
    return int(url.split('/')[-1])
  
  return FreeRankedComic(
    get_comic_id(),
    field,
    get_rank(),
  )



def scrape_free_ranking(driver: WebDriver) -> Ranking:
  URL = 'https://comic.pixiv.net/rankings'
  driver.get(URL)

  def find_fields() -> typing.List[WebElement]:
    return driver.find_elements(
      by=By.CLASS_NAME,
      value='relative',
    )[-1].find_elements(
      by=By.CLASS_NAME,
      value='cursor-pointer',
    )
    

  def get_items() -> typing.List[WebElement]:
    return driver.find_elements(
      by=By.CLASS_NAME,
      value='items-stretch',
    )
  
  ls = []
  fields = find_fields()
  for field in tqdm.tqdm(find_fields()):
    field.click()
    for elm in get_items():
      ls.append(__scrape_free_ranked_comic(field.text, elm))
  return Ranking(datetime.datetime.now(), ls)

