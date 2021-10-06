import dataclasses
import typing
import bs4 
import datetime 


@dataclasses.dataclass
class Episode:
  latest_update: datetime.datetime
  oldest_update: datetime.datetime 
  display_cnt: int



def _scrape_episode(soup: bs4.BeautifulSoup) -> Episode:
  def find_elements() -> typing.NoReturn:
    elements = soup.find_all('a', class_='h-104')
    n = len(elements) // 2
    assert len(elements) == n * 2
    return elements[:n]

  def extract_date(
    elm: bs4.element.Tag,
  ) -> datetime.datetime.date:
    s = elm.find_all('span', class_='text-xs')[-1].text
    s = ''.join(s.split()).lstrip('更新日:')
    return datetime.datetime.strptime(s, '%Y年%m月%d日').date()

  elements = find_elements()
  cnt = len(elements)
  dates = [extract_date(elm) for elm in elements]
  dates.sort()
  oldest = dates[0]
  latest = dates[-1]
  return Episode(latest, oldest, cnt)