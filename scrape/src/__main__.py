
from urllib.robotparser import RobotFileParser
import time
from datetime import datetime
import numpy as np
from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver import (
  ChromeOptions,
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
  options = FirefoxOptions()
  options.headless = True
  # options.add_argument('--no-sandbox')


  driver = webdriver.Firefox(
    options=options,
  )
  return driver


  
def main():
  site_url ="https://comic.pixiv.net/"

  import time
  s = time.time()
  driver = create_driver()

  MakeAdamDFs(driver)()
  driver.close()
  print(time.time() - s)

 

if __name__ == '__main__':
  main()
