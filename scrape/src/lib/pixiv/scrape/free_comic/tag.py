import dataclasses
import typing
import bs4 
import re



@dataclasses.dataclass
class Tag():
  name: str
  cnt: int



def _scrape_tags(soup: bs4.BeautifulSoup) -> typing.List[Tag]:
  ls = soup.find('div', class_='my-16').find(
    class_='px-16',
  ).find_all('span')
  ptn = re.compile(r'^#(.*)\((\d+)\)$')
  tags = []
  for elm in ls:
    elm = ''.join(elm.text.split())
    m = re.match(ptn, elm)
    name = m.group(1)
    cnt = int(m.group(2))
    tag = Tag(name, cnt)
    tags.append(tag)
  return tags

