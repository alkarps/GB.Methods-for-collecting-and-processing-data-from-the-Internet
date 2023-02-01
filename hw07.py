from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import time


s = Service('./chromedriver')

chromeOptions = Options()
chromeOptions.add_argument('start-maximized')


driver = webdriver.Chrome(service=s, options=chromeOptions)
driver.implicitly_wait(10)
driver.get("https://www.mvideo.ru/")
WebDriverWait(driver, 40)\
    .until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'app-header-contactbar')]")))
driver.execute_script("window.scrollTo(0, 1000)")
ActionChains(driver).scroll_by_amount(0,2000)\
    .move_by_offset(0,1)\
    .click(driver.find_element(By.XPATH, "//button[@class='tab-button ng-star-inserted']"))
time.sleep(1)
goods_title = driver.find_elements(By.XPATH,"//mvid-product-cards-group[@_ngcontent-serverapp-c229]//div[@class='title']//div//text()")
goods_price = driver.find_elements(By.XPATH,"//mvid-product-cards-group[@_ngcontent-serverapp-c229]//span[@class='price__main-value']/text()")
goods_url = driver.find_elements(By.XPATH,"//mvid-product-cards-group[@_ngcontent-serverapp-c229]//a[@class='img-with-badge']/@href")
db_goods = MongoClient('mongodb://127.0.0.1:27017/').goods
for i in range(len(goods_url)):
    db_goods.insert_one({"name":goods_title[i], "price":goods_price[i], "url": goods_url[i]})