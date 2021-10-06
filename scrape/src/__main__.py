import time
from selenium.webdriver import (
  Firefox,
  FirefoxOptions,
)
from selenium.webdriver.remote.webdriver import WebDriver
import time
from lib.adam import (
  add_ranked_comics,
  update_ranked_comics,
)


def create_driver() -> WebDriver:
  options = FirefoxOptions()
  options.headless = True
  return Firefox(options=options)


def main():
  s = time.time()
  driver = create_driver()
  add_ranked_comics(driver)
  driver.close()
  update_ranked_comics()
  print(time.time() - s)

 

if __name__ == '__main__':
  main()