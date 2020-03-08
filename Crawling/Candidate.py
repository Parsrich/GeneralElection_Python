import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# from bs4 import BeautifulSoup
# from urllib.request import urlopen
# import pyperclip
import time
# import datetime


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

driver = webdriver.Chrome('/Users/kyome/dev/Parsrich/GeneralElection/python/Crawling/chromedriver')
driver.get("http://info.nec.go.kr/main/showDocument.xhtml?electionId=0020200415&topMenuId=PC&secondMenuId=PCRI03")
driver.maximize_window()
driver.find_element_by_xpath('//*[@id="electionId2"]').click()
time.sleep(1)


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
cityOptions = soup.select('#cityCode > option')
cityCodes = [ o['value'] for o in cityOptions][1:]

for code in cityCodes:
    driver.find_element_by_xpath('//*[@id="cityCode"]').click()
    driver.find_element_by_css_selector('#cityCode > [value="'+code+'"]').click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    sggCityOptions = soup.select('#sggCityCode > option')
    sggCityCodes = [o['value'] for o in sggCityOptions][1:]
    for sggCode in sggCityCodes:
        driver.find_element_by_xpath('//*[@id="sggCityCode"]').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#sggCityCode > [value="' + sggCode + '"]').click()
        WebDriverWait(driver,15).until(EC.presence_of_element_located((By.ID, "spanSubmit"))).click()


# print([ o['value'] for o in cityOptions])
# if unknownTag != None:
#     # 제품 정보 객체 초기화
#     tempDetailInfo = dict()
#     tempDetailInfo['title'] = ""


# driver.find_element_by_xpath('//*[@id="cityCode"]').click()


# element = WebDriverWait(driver,15).until(
#          EC.presence_of_element_located((By.CLASS_NAME, "header-brand")))
# electionId2

# doc_ref = db.collection(u'users').document(u'alovelace')
# doc_ref.set({
#     u'first': u'Ada',
#     u'last': u'Lovelace',
#     u'born': 1815
# })

# users_ref = db.collection(u'users')
# docs = users_ref.stream()
#
# for doc in docs:
#     print(u'{} => {}'.format(doc.id, doc.to_dict()))

# print (firebase_admin)
#
# https://generalelection-6a43a.firebaseio.com