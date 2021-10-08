import typing 
from selenium.webdriver.remote.webdriver import (
  WebDriver,
)
import datetime 
import pandas as pd 
from lib.pixiv.scrape import (
  scrape_free_ranking,
)
from lib.aws_util.s3.upload import (
  upload_to_s3,
)
from lib.aws_util.s3.download import (
  download_from_s3,
)


def add_ranked_comics(driver: WebDriver) -> typing.NoReturn:
  ranking = scrape_free_ranking(driver)
  df = pd.DataFrame(ranking.comics)
  df['ranked_at'] = ranking.datetime.date()
  _store_to_s3(df)


def _store_to_s3(df: pd.DataFrame) -> typing.NoReturn:
  bucket = 'av-adam-store'
  save_path = '/tmp/ranked_comics.csv'
  upload_obj = 'pixiv/ranked_comics.csv'
  dt = datetime.datetime.now()
  df['updated_at'] = str(dt.date())
  download_from_s3(bucket, upload_obj, save_path)
  old_rank = pd.read_csv(save_path)
  df = pd.concat((old_rank, df), ignore_index=True)
  df['ranked_at'] = df['ranked_at'].astype(str)
  df['rank'] = df['rank'].astype(int)
  df['comic_id'] = df['comic_id'].astype(int)
  df.drop_duplicates(
    subset=['comic_id', 'field', 'rank', 'ranked_at'],
    keep='last',
    inplace=True,
  ) 
  print(df)
  df.to_csv(save_path, index=False)
  upload_to_s3(bucket, upload_obj, save_path)
  
