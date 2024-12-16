import time
import random
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
chromedriver_path = r"chromedriver-win64\chromedriver.exe"

options = Options()
options.binary_location = brave_path
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)

url = "https://www.wcostream.tv/adventure-time-season-1-episode-1-slumber-party-panic" # starts at first episode
driver.get(url)

# scroll down the page by  500 pixel vertical
driver.execute_script("window.scrollTo(0, 500);")

time.sleep(1)

episode_title_element = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td[1]/table/tbody/tr/td/table[1]/tbody/tr[1]/td/h1/a')
title = episode_title_element.text
print(title)

video_container = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe#frameNewcizgifilmuploads0'))
)
video_container.click()
time.sleep(random.uniform(4, 7))

driver.switch_to.frame(video_container)

episode = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.TAG_NAME, "video"))
)

# right click
actions = ActionChains(driver)
actions.move_to_element(episode).context_click().perform()
time.sleep(random.uniform(1, 2))

for _ in range(5):
    # go to Save as... option
    pyautogui.press('down')

# press enter when Save as... option is selected
pyautogui.press('enter')

# wait cos my human eyes are not following
time.sleep(random.uniform(5, 7))

pyautogui.press('backspace')
pyautogui.write(title)

# download
pyautogui.press('enter')

time.sleep(random.uniform(2, 6))

# random numbers to wait for download to finish
time.sleep(random.uniform(480, 620))

driver.quit()