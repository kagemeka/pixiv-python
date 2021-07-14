

from \
  selenium.webdriver.remote \
  .webdriver \
import (
  WebDriver,
)
from \
  kgmk.pixiv.scrape \
  .ranked_free_comic \
import (
  ScrapeRankedFreeComics,
  RankedFreeComic,
)

import dataclasses
import typing

import requests
import bs4 
import pandas as pd




class MakeGenreDF():
  
  def __call__(
    self,
    comic: RankedFreeComic,
  ) -> pd.DataFrame:
    self.__comic = comic
    self.__make()
    return self.__df


  def __make(
    self,
  ) -> typing.NoReturn:
    comic = self.__comic
    id_ = comic.comic_id
    genres = (
      comic.summary.genres
    )
    self.__df = pd.DataFrame({
      'comic_id': id_,
      'genre': genres,
    })



class MakeTagDF():
  
  def __call__(
    self,
    comic: RankedFreeComic,
  ) -> pd.DataFrame:
    self.__comic = comic
    self.__make()
    return self.__df 


  def __make(
    self,
  ) -> typing.NoReturn:
    comic = self.__comic
    tags = [
      (tag.name, tag.cnt)
      for tag in comic.tags
    ]
    df = pd.DataFrame(
      tags,
      columns=['name', 'cnt'],
    )
    id_ = comic.comic_id
    df['comic_id'] = id_
    self.__df = df


  

class MakeMetaDF():
  
  def __call__(
    self,
    comic: RankedFreeComic,
  ) -> pd.DataFrame:
    self.__comic = comic
    self.__make()
    return self.__df
  
  def __make(
    self,
  ) -> typing.NoReturn:
    comic = self.__comic
    meta = comic.metadata
    smry = comic.summary
    epi = comic.episode 
    data = {
      'comic_id': comic.comic_id,
      'title': meta.title,
      'author_text': meta.author_text,
      'magazine': meta.magazine,
      'overview': smry.overview,
      'ranked_field': comic.ranked_field,
      'rank': comic.rank,
      'episode_cnt': epi.display_cnt,
      'latest_update': epi.latest_update,
      'oldest_update': epi.oldest_update,
      'follower_cnt': smry.follower_cnt,
    }
    self.__df = pd.DataFrame(
      [[*data.values()]],
      columns=[*data.keys()],
    )





@dataclasses.dataclass
class AdamDF():
  meta: pd.DataFrame
  genre: pd.DataFrame
  tag: pd.DataFrame


class MakeAdamDF():

  def __call__(
    self,
    comic: RankedFreeComic,
  ) -> AdamDF:
    self.__comic = comic
    self.__make()
    return self.__adam_df
    
  
  def __make(
    self,
  ) -> typing.NoReturn:
    comic = self.__comic
    meta = MakeMetaDF()(comic)
    tag = MakeTagDF()(comic)
    genre = MakeGenreDF()(
      comic,
    )
    self.__adam_df = AdamDF(
      meta,
      genre,
      tag,
    )




import os
import boto3
from datetime import (
  datetime,
)


class MakeAdamDFs():

  def __call__(
    self,
  ) -> AdamDF:
    self.__scrape()
    self.__make()
    self.__add_timestamp()
    self.__store()
    # self.__upload()
  

  def __init__(
    self,
    driver: WebDriver,
  ) -> typing.NoReturn:
    self.__driver = driver
    dt = datetime.now()
    self.__dt = dt 
    date = dt.date()
    self.__save_dir = (
      f'/tmp/'
    )
    self.__upload_dir = (
      f'pixiv/{date}/'
    )


  def __scrape(
    self,
  ) -> typing.NoReturn:
    f = ScrapeRankedFreeComics(
      self.__driver,
    )
    self.__comics = f()

  
  def __make(
    self,
  ) -> typing.NoReturn:
    meta = []
    genre = []
    tag = []
    f = MakeAdamDF()
    for comic in self.__comics:
      df = f(comic)
      meta.append(df.meta)
      genre.append(df.genre)
      tag.append(df.tag)
    meta = pd.concat(
      meta,
      ignore_index=True,
    )
    genre = pd.concat(
      genre,
      ignore_index=True,
    )
    tag = pd.concat(
      tag,
      ignore_index=True,
    )
    self.__df = AdamDF(
      meta,
      genre,
      tag,
    )

  
  def __add_timestamp(
    self,
  ) -> typing.NoReturn:
    df = self.__df
    dt = self.__dt
    df.meta['datetime'] = dt
    df.genre['datetime'] = dt
    df.tag['datetime'] = dt
    self.__df = df
  
  
  def __store(
    self,
  ) -> typing.NoReturn:
    d = self.__save_dir
    os.makedirs(d, exist_ok=1)
    df = self.__df
    meta_path = (
      f'{d}pixiv_meta.csv'
    )
    df.meta.to_csv(
      meta_path, 
      index=False,
    )
    genre_path = (
      f'{d}pixiv_genre.csv'
    )
    df.genre.to_csv(
      genre_path,
      index=False,
    )
    tag_path = (
      f'{d}pixiv_tag.csv'
    )
    df.tag.to_csv(
      tag_path,
      index=False,
    )
    (
      self.__meta_path,
      self.__genre_path,
      self.__tag_path,
    ) = (
      meta_path,
      genre_path,
      tag_path,
    )


  def __upload(
    self,
  ) -> typing.NoReturn:
    (
      meta_path,
      genre_path,
      tag_path,
    ) = (
      self.__meta_path,
      self.__genre_path,
      self.__tag_path,
    )
    d = self.__upload_dir
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(
      'av-adam-entrance',
    )
    bucket.Object(
      f'{d}pixiv_meta.csv',
    ).upload_file(
      meta_path,
    )
    bucket.Object(
      f'{d}pixiv_genre.csv',
    ).upload_file(
      genre_path,
    )
    bucket.Object(
      f'{d}pixiv_tag.csv',
    ).upload_file(
      tag_path,
    )
  