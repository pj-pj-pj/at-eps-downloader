import os
import time
import random
import pyautogui
import re
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

browser_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
driver_path = r"edgedriver_win64/msedgedriver.exe"
downloads_folder = r"C:\Users\peaks\downloads"

def is_download_complete(folder):
    while True:
        files = os.listdir(folder)
        downloading = any(file.endswith(('.crdownload', '.tmp', '.part')) for file in files)

        if not downloading:
            break
        time.sleep(1)

url = "https://www.wcostream.tv/adventure-time-season-1-episode-1-slumber-party-panic"  # starts at first episode

# test for last episode to see what happens if there is no next episode
# if else statement below is useless -> IT BREAKS
# url = "https://www.wcostream.tv/adventure-time-distant-lands-episode-4-wizard-city"

while True:
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(driver_path), options=options)

    try:
        driver.get(url)

        # scroll down the page by  500 pixel vertical
        driver.execute_script("window.scrollTo(0, 500);")

        time.sleep(1)

        episode_title_element = driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody/tr/td[1]/table/tbody/tr/td/table[1]/tbody/tr[1]/td/h1/a')
        title = episode_title_element.text
        title = re.sub(r'[^a-zA-Z0-9]', '_', title)
        print(title)

        video_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe#frameNewcizgifilmuploads0'))
        )
        video_container.click()
        time.sleep(random.uniform(20, 35))

        driver.switch_to.frame(video_container)

        episode = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )

        # right click
        actions = ActionChains(driver)
        actions.move_to_element(episode).context_click().perform()
        time.sleep(random.uniform(1, 3))

        for _ in range(4):
            # go to Save as... option
            pyautogui.press('down')

        # press enter when Save as... option is selected
        pyautogui.press('enter')

        # wait cos my human eyes are not following
        time.sleep(6)

        pyautogui.press('backspace')
        pyautogui.write(title)

        # download
        pyautogui.press('enter')

        print("Waiting for download to complete...")
        is_download_complete(downloads_folder)
        print("Download complete!")

        driver.switch_to.parent_frame()

        next_episode = driver.find_elements(By.CSS_SELECTOR, "tbody tr:nth-of-type(2) td:nth-of-type(2) a")

        if next_episode:
            url = next_episode[0].get_attribute('href')
            print(f"Next ep: {url}")

            driver.quit()
        else:
            print(f"No Next Episode.")
            break
    except Exception as e:
        print(f"Error occurred: {e}")
        break