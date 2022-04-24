# Вариант II
# 2) Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД.
#     Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары
#
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient


# client = MongoClient('127.0.0.1', 27017)
# db = client['mvideo']
# mvideo_db = db.mvideo
options = Options()
options.add_argument("start-maximized")
s = Service('./chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)
driver.get('https://www.mvideo.ru/')
actions = ActionChains(driver)

actions.click()

try:
    actions.key_down(Keys.SPACE).key_up(Keys.SPACE).key_down(Keys.SPACE).key_up(Keys.SPACE)
    actions.perform()
    time.sleep(5)
    button = driver.find_element(By.XPATH, "//button[@class ='tab-button ng-star-inserted']")
    button.click()
except ElementClickInterceptedException:
    print('кнопка потерялась')

goods = driver.find_elements(By.XPATH, "//mvid-shelf-group//mvid-product-cards-group//div[@class='title']]")
for good in goods:
    trend = good.find_element(By.TAG_NAME, "div").text
    print(trend)

# for i in trend:
#     mvideo_db.insert_one(i)

# ElementClickInterceptedException