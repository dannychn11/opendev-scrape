from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import os
import datetime

# setup
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

# Open site and get links and names for builds
driver.get("https://review.opendev.org/c/openstack/manila/+/905728?tab=change-view-tab-header-zuul-results-summary")
el = driver.find_element(By.TAG_NAME,"gr-app").shadow_root.find_element(By.CSS_SELECTOR,"gr-app-element").shadow_root.find_element(By.CSS_SELECTOR, "gr-change-view").shadow_root
links = el.find_element(By.CSS_SELECTOR, "zuul-summary-status-tab").shadow_root.find_elements(By.CSS_SELECTOR, 'a')
urls = [link.get_attribute('href') + "/logs" for link in links]
names = [link.get_attribute('innerHTML') + str(datetime.datetime.now().isoformat()) for link in links]

# Set path for logs folder
script_dir = os.path.dirname(__file__)
path = os.path.join(script_dir, './logs')
if not os.path.exists(path):
    os.makedirs(path)

# Go to each build and write the JSON to a new log file
for i in range(len(urls)):
    newURL, newName = urls[i], names[i]
    try:
        driver.get(newURL)
        time.sleep(3)
        joblink = driver.find_element(By.XPATH, "//span[contains(text(),'job-output.json')]")
        joblink.find_element(By.TAG_NAME, "a").click()
        json = driver.find_element(By.TAG_NAME, "pre").get_attribute('innerHTML')
        with open(os.path.join(path, names[i]), 'w') as temp_file:
            temp_file.write(json)
    except:
        print('failed to download from: ', newURL)
driver.close()