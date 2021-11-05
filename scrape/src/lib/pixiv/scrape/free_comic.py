import dataclasses
import re
import typing
import requests
import bs4
import datetime
import tqdm


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

    def extract_date(elm: bs4.element.Tag) -> datetime.datetime.date:
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


@dataclasses.dataclass
class Summary():
    overview: str
    follower_cnt: int
    genres: typing.List[str]


def _scrape_summary(soup: bs4.BeautifulSoup) -> Summary:
    def get_overview() -> str:
        return soup.find(class_='jsx-3803037064').text

    def get_follower_cnt() -> int:
        elm = soup.find('div', class_='my-16').find('div', class_='items-center')
        return int(elm.text.replace(',', ''))

    def get_genres() -> typing.List[str]:
        elm = soup.find('div', class_='my-16').find('div', class_='ml-16')
        return [e.text for e in elm.find_all('span')]

    return Summary(get_overview(), get_follower_cnt(), get_genres())


@dataclasses.dataclass
class Metadata:
    title: str
    author_text: str
    magazine: str


def _scrape_metadata(soup: bs4.BeautifulSoup) -> Metadata:
    def get_title() -> str:
        return soup.find('h1').text

    def get_author_text() -> str:
        return soup.find('div', class_='mt-4').text

    def get_magazine() -> str:
        return soup.find(
            class_='screen4:bg-surface2-default',
        ).find('span', class_='text-xs').text

    print(get_magazine())
    return Metadata(get_title(), get_author_text(), get_magazine())


@dataclasses.dataclass
class Tag():
    name: str
    cnt: int


def _scrape_tags(soup: bs4.BeautifulSoup) -> typing.List[Tag]:
    ls = soup.find('div', class_='my-16').find(class_='px-16').find_all('span')
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


@dataclasses.dataclass
class FreeComic():
    comic_id: int
    metadata: Metadata
    summary: Summary
    tags: typing.List[Tag]
    episode: Episode


def scrape_free_comic(comic_id: int) -> typing.Optional[FreeComic]:
    BASE_URL = 'https://comic.pixiv.net/works/'
    response = requests.get(f'{BASE_URL}/{comic_id}')
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(response.content, 'html.parser')
    if soup.find(class_='error') is not None: return None
    if 'お探しのページは見つかりませんでした。' in soup.text: return None
    return FreeComic(
        comic_id,
        _scrape_metadata(soup),
        _scrape_summary(soup),
        _scrape_tags(soup),
        _scrape_episode(soup),
    )


def scrape_free_comics(comic_ids: typing.List[int]) -> typing.Iterator[FreeComic]:
    for id_ in tqdm.tqdm(comic_ids):
        print(id_)
        comic = scrape_free_comic(id_)
        if comic is None: continue
        yield comic 
