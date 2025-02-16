import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os
from selenium.webdriver.common.by import By

# Redirect Chrome logging to devnull
os.environ['WDM_LOG_LEVEL'] = '0'

# Setup Chrome options with complete silence
chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--silent')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.youtube.com/watch?v=iYOTRSMza6o")

# Scroll to load in all the comments
time.sleep(7)
while True:
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1)
    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    print(f"Page scrolled from {last_height} to {new_height}")
    if new_height == last_height:
        print("Reached bottom of page")
        break

print("Container scrolling complete")
time.sleep(2)

num_comments = len(driver.find_elements(By.CSS_SELECTOR, "#contents > ytd-comment-thread-renderer"))

print(f"Found {num_comments} comments")

comments_list = []
for comment in WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
        comments_list.append(comment.text)

#content-text > span

#content-text > span

with open("comments.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["Comment"])
    writer.writeheader()
    for comment in comments_list:
        writer.writerow({"Comment": comment})  # changed to wrap comment string in a dict

driver.quit()