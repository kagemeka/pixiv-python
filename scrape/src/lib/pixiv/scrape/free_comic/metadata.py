import dataclasses
import typing
import bs4


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
    return Metadata(
        get_title(),
        get_author_text(),
        get_magazine(),
    )
