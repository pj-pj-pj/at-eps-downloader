import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
chromedriver_path = r"chromedriver-win64\chromedriver.exe"

options = Options()
options.binary_location = brave_path
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

url = "https://www.wcostream.tv/adventure-time-pilot" # starts at first/pilot episode
driver.get(url)

time.sleep(5)

driver.quit()