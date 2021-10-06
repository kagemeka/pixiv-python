import time
from selenium.webdriver import (
  Chrome,
  ChromeOptions,
)
from selenium.webdriver.remote.webdriver import WebDriver
from lib.adam import (
  add_ranked_comics,
  update_ranked_comics,
)



def create_driver() -> WebDriver:
  opt = ChromeOptions()
  opts = [
    '--no-sandbox',
    '--single-process',
    '--disable-dev-shm-usage',
    '--homedir=/tmp',
  ]
  opt.headless = True
  for o in opts: opt.add_argument(o)
  opt.binary_location = '/opt/headless-chromium'
  return Chrome('/opt/chromedriver', options=opt)


def lambda_handler(event, context):
  driver = create_driver()
  add_ranked_comics(driver)
  driver.close()
  update_ranked_comics()
  return {
    "statusCode": 200,
    "body": 'success',
  }
