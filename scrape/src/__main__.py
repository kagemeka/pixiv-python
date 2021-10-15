import selenium.webdriver
import time
from lib import adam


def create_driver() -> selenium.webdriver.remote.webdriver.WebDriver:
    options = selenium.webdriver.FirefoxOptions()
    options.headless = True
    return selenium.webdriver.Firefox(options=options)


def main():
    s = time.time()
    driver = create_driver()
    adam.add_ranked_comics(driver)
    driver.close()
    adam.update_ranked_comics()
    print(time.time() - s)


if __name__ == '__main__':
    main()
