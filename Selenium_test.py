from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

'''path to webdriver: "C:/Users/66ase/PycharmProjects/pythonProject/venv/Lib/site-packages/selenium/webdriver'
                           "/chrome/chromedriver.exe"'''
# open login page
browser = webdriver.Chrome()
browser.get("https://www.eiger.io/signin")
# find login and password elements
username = browser.find_element(By.ID, "email")
password = browser.find_element(By.ID, "Password")
# enter login credentials
username.send_keys("artem@tritoninnovation.com")
password.send_keys("adgjmptw3D!")
# execute click() on log in button
browser.find_element(By.XPATH, "//input[@type='submit']").click()
# wait until page is loaded
element = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, "navbar-devices-link")))
# if page is loaded, open printer's status page
if element:
    print(f"Status: {element}")
    browser.get("https://www.eiger.io/device/33b99c92-984a-44f3-bbca-550167b405ad")
# wait until page is loaded
element = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, "//div[@class='form-table']")))
# wait extra time to ensure that page is loaded
time.sleep(7)
# locate Pause button and execute click() action
if element:
    print(f"Status: {element}")
    browser.find_element(By.XPATH, "//div[@class='device-detail-actions-group']//button[3]").click()
    browser.close()
