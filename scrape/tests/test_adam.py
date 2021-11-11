import typing
import sys
import time
from selenium.webdriver import (
    Chrome,
    ChromeOptions,
    Firefox,
    FirefoxOptions,
)
import selenium.webdriver 

def create_driver() -> selenium.webdriver.remote.webdriver.WebDriver:
    options = FirefoxOptions()
    options.headless = True
    return Firefox(options=options)


def set_globals() -> typing.NoReturn:
    import os
    global cfd, root
    cfd = os.path.abspath(os.path.dirname(__file__))
    root = os.path.abspath(f'{cfd}/..')


set_globals()
sys.path.append(f'{root}/src')


from lib.adam import (
    add_ranked_comics,
    update_ranked_comics,
)



def test_add_ranked_comic_ids() -> typing.NoReturn:
    driver = create_driver()
    add_ranked_comics(driver)
    driver.close()


def test_update_ranked_comics() -> typing.NoReturn:
    update_ranked_comics()


if __name__ == '__main__':
    test_add_ranked_comic_ids()
    test_update_ranked_comics()
