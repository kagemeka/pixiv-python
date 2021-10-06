import dataclasses
import typing
import requests
import bs4 
from .metadata import Metadata, _scrape_metadata
from .episode import Episode, _scrape_episode
from .tag import Tag, _scrape_tags
from .summary import Summary, _scrape_summary 



@dataclasses.dataclass
class FreeComic():
  comic_id: int
  metadata: Metadata
  summary: Summary
  tags: typing.List[Tag]
  episode: Episode



def scrape_free_comic(comic_id: int) -> FreeComic:
    BASE_URL = 'https://comic.pixiv.net/works/'
    response = requests.get(f'{BASE_URL}/{comic_id}')
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    return FreeComic(
      comic_id,
      _scrape_metadata(soup),
      _scrape_summary(soup),
      _scrape_tags(soup),
      _scrape_episode(soup),
    )

