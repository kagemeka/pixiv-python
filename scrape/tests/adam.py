import typing
import sys
import time
from selenium.webdriver import (
    Chrome,
    ChromeOptions,
    Firefox,
    FirefoxOptions,
)
from selenium.webdriver.remote.webdriver import WebDriver


def create_driver() -> WebDriver:
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


try:
    from lib.adam import (
        add_ranked_comics,
        update_ranked_comics,
    )
except Exception:
    pass


def test_add_ranked_comic_ids() -> typing.NoReturn:
    driver = create_driver()
    add_ranked_comics(driver)
    driver.close()


def test_update_ranked_comics() -> typing.NoReturn:
    update_ranked_comics()


if __name__ == '__main__':
    test_add_ranked_comic_ids()
    test_update_ranked_comics()
