import dataclasses
import typing
import bs4 



@dataclasses.dataclass
class Summary():
  overview: str
  follower_cnt: int
  genres: typing.List[str]



def _scrape_summary(soup: bs4.BeautifulSoup) -> Summary:
  def get_overview() -> str:
    return soup.find(class_='jsx-3803037064').text 

  def get_follower_cnt() -> int:
    elm = soup.find('div', class_='my-16')
    elm = elm.find('div', class_='items-center')
    return int(elm.text.replace(',', ''))
 
  def get_genres() -> typing.List[str]:
    elm = soup.find('div', class_='my-16')
    elm = elm.find('div', class_='ml-16')
    return [e.text for e in elm.find_all('span')]
  
  return Summary(
    get_overview(),
    get_follower_cnt(),
    get_genres(),
  )
