import time
from selenium.webdriver import (
  Chrome,
  ChromeOptions,
  Firefox,
  FirefoxOptions,
)
from \
  selenium.webdriver.remote \
  .webdriver \
import (
  WebDriver,
)
from lib.adam import (
  MakeAdamDFs,
)




def create_driver(
) -> WebDriver:
  opt = ChromeOptions()
  opts = [
    '--no-sandbox',
    '--single-process',
    '--disable-dev-shm-usage',
    '--homedir=/tmp',
  ]
  opt.headless = True
  for o in opts:
    opt.add_argument(o)
  opt.binary_location = (
    '/opt/headless-chromium'
  )
  driver = Chrome(
    '/opt/chromedriver',
    options=opt,
  )
  return driver


def lambda_handler(
  event, 
  context,
):
  driver = create_driver()
  MakeAdamDFs(driver)()
  driver.close()
  return {
    "statusCode": 200,
    "body": 'success',
  }


# def create_driver(
# ) -> WebDriver:
#   options = FirefoxOptions()
#   options.headless = True
#   # options.add_argument('--no-sandbox')


#   driver = webdriver.Firefox(
#     options=options,
#   )
#   return driver


  
def main():
  site_url ="https://comic.pixiv.net/"

  import time
  s = time.time()
  driver = create_driver()

  MakeAdamDFs(driver)()
  driver.close()
  print(time.time() - s)

 

# if __name__ == '__main__':
#   main()