from selenium import webdriver
from bs4 import BeautifulSoup
import gspread
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials
import time

browser = webdriver.Chrome()
url = "http://twinge.tv/channels/ninja/games/#/7"
browser.get(url) #navigate to the page
time.sleep(5) #allow js to load
innerHTML = browser.page_source
browser.get("http://twinge.tv/channels/ninja/")
time.sleep(5) #allow js to load
innerHTML = browser.page_source
url = "http://twinge.tv/channels/ninja/games/#/90"
browser.get(url) #navigate to the page
time.sleep(5) #allow js to load
innerHTML = browser.execute_script("return document.body.innerHTML")
print (games)
