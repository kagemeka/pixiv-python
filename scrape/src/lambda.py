import selenium.webdriver
import typing
from lib import adam


def create_driver() -> selenium.webdriver.remote.webdriver.WebDriver:
    opt = selenium.webdriver.ChromeOptions()
    opts = [
        '--no-sandbox',
        '--single-process',
        '--disable-dev-shm-usage',
        '--homedir=/tmp',
    ]

    opt.headless = True
    for o in opts:
        opt.add_argument(o)
    opt.binary_location = '/opt/headless-chromium'
    return selenium.webdriver.Chrome('/opt/chromedriver', options=opt)


def lambda_handler(event, context) -> typing.NoReturn:
    driver = create_driver()
    adam.add_ranked_comics(driver)
    driver.close()
    adam.update_ranked_comics()
    return {
        "statusCode": 200,
        "body": 'success',
    }
