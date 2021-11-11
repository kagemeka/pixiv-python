import typing
import sys
import selenium.webdriver


def create_driver() -> selenium.webdriver.remote.webdriver.WebDriver:
    options = selenium.webdriver.FirefoxOptions()
    options.headless = True
    return selenium.webdriver.Firefox(options=options)


def set_globals() -> typing.NoReturn:
    import os
    global cfd, root
    cfd = os.path.abspath(os.path.dirname(__file__))
    root = os.path.abspath(f'{cfd}/../..')


set_globals()
sys.path.append(f'{root}/src')

from lib.pixiv.scrape import scrape_free_comic
from lib.pixiv.scrape import scrape_free_ranking

from lib.pixiv.scrape import scrape_free_comics
# import lib.pixiv.scrape 

def test_scrape_free_ranking() -> typing.NoReturn:
    driver = create_driver()
    ranking = scrape_free_ranking(driver)
    driver.close()
    print(ranking)


def test_scrape_free_comic() -> typing.NoReturn:
    comic_id = 7800
    comic = scrape_free_comic(comic_id)
    print(comic)


def test_scrape_free_comics() -> typing.NoReturn:
    comic_ids = [7800, 7891, 6580]
    comics = scrape_free_comics(comic_ids)
    for comic in comics:
        print(comic)
         

if __name__ == '__main__':
    test_scrape_free_ranking()
    test_scrape_free_comic()
    test_scrape_free_comics()