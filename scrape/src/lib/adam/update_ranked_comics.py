import typing 
import datetime 
import pandas as pd 
import dataclasses 
from lib.pixiv.scrape import (
  scrape_free_comics,
)
from lib.pixiv.scrape.free_comic import FreeComic
from lib.aws_util.s3.upload import (
  upload_to_s3,
)
from lib.aws_util.s3.download import (
  download_from_s3,
)




def _fetch_ranked_comic_ids() -> typing.List[int]:
  bucket = 'av-adam-store'
  save_path = '/tmp/ranked_comics.csv'
  obj = 'pixiv/ranked_comics.csv'
  download_from_s3(bucket, obj, save_path)
  df = pd.read_csv(save_path)
  return list(df.comic_id.unique())
  

def update_ranked_comics() -> typing.NoReturn:
  comic_ids = _fetch_ranked_comic_ids()
  comics = scrape_free_comics(comic_ids)
  df = MakeComicDataFrame().from_comics(comics)
  print(df)
  _store_to_s3(df)



@dataclasses.dataclass
class ComicDataFrame():
  meta: pd.DataFrame
  genre: pd.DataFrame
  tag: pd.DataFrame
  



class MakeComicDataFrame():
  def __make_meta(self, comic: FreeComic) -> pd.DataFrame:
    meta = comic.metadata
    summary = comic.summary
    episode = comic.episode 
    data = {
      'comic_id': comic.comic_id,
      'title': meta.title,
      'author_text': meta.author_text,
      'magazine': meta.magazine,
      'overview': summary.overview,
      'episode_cnt': episode.display_cnt,
      'latest_update': episode.latest_update,
      'oldest_update': episode.oldest_update,
      'follower_cnt': summary.follower_cnt,
    }
    return pd.DataFrame(
      [[*data.values()]],
      columns=[*data.keys()],
    )
  

  def __make_genre(self, comic: FreeComic) -> pd.DataFrame:
    return pd.DataFrame({
      'comic_id': comic.comic_id,
      'genre': comic.summary.genres,
    })


  def __make_tag(self, comic: FreeComic) -> pd.DataFrame:
    tags = [(tag.name, tag.cnt) for tag in comic.tags]
    df = pd.DataFrame(
      tags,
      columns=['name', 'cnt'],
    )
    df['comic_id'] = comic.comic_id
    return df 


  def from_comic(self, comic: FreeComic) -> ComicDataFrame:
    return ComicDataFrame(
      self.__make_meta(comic),
      self.__make_genre(comic),
      self.__make_tag(comic),
    )
  

  def from_comics(
    self, 
    comics: typing.Iterable[FreeComic],
  ) -> typing.Optional[ComicDataFrame]:
    meta, genre, tag = [], [], []
    for comic in comics:
      df = self.from_comic(comic)
      meta.append(df.meta)
      genre.append(df.genre)
      tag.append(df.tag)
    if not meta: return None
    return ComicDataFrame(
      pd.concat(meta),
      pd.concat(genre),
      pd.concat(tag),
    )


def _store_to_s3(df: ComicDataFrame) -> typing.NoReturn:
  dt = datetime.datetime.now()
  date = str(dt.date())
  bucket = 'av-adam-store'
  save_dir = '/tmp/'
  upload_dir = f'pixiv/'
  meta_path = f'{save_dir}meta.csv'
  meta_obj = f'{upload_dir}meta.csv'
  genre_path = f'{save_dir}genre.csv'
  genre_obj = f'{upload_dir}genre.csv'
  tag_path = f'{save_dir}tag.csv'
  tag_obj = f'{upload_dir}tag.csv'

  def add_timestamp() -> typing.NoReturn:
    df.meta['updated_at'] = date
    df.genre['updated_at'] = date
    df.tag['updated_at'] = date

  def download() -> typing.NoReturn:
    download_from_s3(bucket, meta_obj, meta_path)
    download_from_s3(bucket, genre_obj, genre_path)
    download_from_s3(bucket, tag_obj, tag_path)

  def merge() -> typing.NoReturn:
    meta_old = pd.read_csv(meta_path)
    meta = pd.concat((meta_old, df.meta), ignore_index=True)
    meta.drop_duplicates(
      subset=['comic_id', 'updated_at'], 
      keep='last',
      inplace=True,
    )
    print(meta)
    meta.to_csv(meta_path, index=False)
 
    genre_old = pd.read_csv(genre_path)
    genre = pd.concat((genre_old, df.genre), ignore_index=True)
    genre.drop_duplicates(
      subset=['comic_id', 'genre', 'updated_at'], 
      keep='last',
      inplace=True,
    )
    print(genre)
    genre.to_csv(genre_path, index=False)

    tag_old = pd.read_csv(tag_path)
    tag = pd.concat((tag_old, df.tag), ignore_index=True)
    tag.drop_duplicates(
      subset=['comic_id', 'name', 'updated_at'], 
      keep='last',
      inplace=True,
    )
    print(tag)
    tag.to_csv(tag_path, index=False)


  def upload() -> typing.NoReturn:
    upload_to_s3(bucket, meta_obj, meta_path)
    upload_to_s3(bucket, genre_obj, genre_path)
    upload_to_s3(bucket, tag_obj, tag_path)

  add_timestamp()
  # df.meta.to_csv(meta_path, index=False)
  # df.genre.to_csv(genre_path, index=False)
  # df.tag.to_csv(tag_path, index=False)
  download()
  merge()
  upload()