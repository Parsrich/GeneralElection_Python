import firebase_admin
import re
from firebase_admin import firestore
from firebase_admin import credentials
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

driver = webdriver.Chrome('/Users/kyome/dev/Parsrich/GeneralElection/python/Crawling/chromedriver')
driver.get("http://info.nec.go.kr/main/showDocument.xhtml?electionId=0020200415&topMenuId=PC&secondMenuId=PCRI03")
driver.maximize_window()
re.compile('(.*)')

# 국회의원선거

driver.find_element_by_xpath('//*[@id="electionId2"]').click()
time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
cityOptions = soup.select('#cityCode > option')
cityCodes = [ o['value'] for o in cityOptions][1:]

for code in cityCodes:
    driver.find_element_by_xpath('//*[@id="cityCode"]').click()
    tempSi = driver.find_element_by_css_selector('#cityCode > [value="' + code + '"]').text
    driver.find_element_by_css_selector('#cityCode > [value="'+code+'"]').click()

    time.sleep(0.5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    sggCityOptions = soup.select('#sggCityCode > option')
    sggCityCodes = [o['value'] for o in sggCityOptions][1:]
    for sggCode in sggCityCodes:
        driver.find_element_by_xpath('//*[@id="sggCityCode"]').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('#sggCityCode > [value="' + sggCode + '"]').click()
        tempGu = driver.find_element_by_css_selector('#sggCityCode > [value="' + sggCode + '"]').text
        WebDriverWait(driver,15).until(EC.presence_of_element_located((By.ID, "spanSubmit"))).click()

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        resultTable = soup.select('#table01 > tbody > tr')

        for tr in resultTable:
            temp = dict()
            href = tr.select('td')[3].select('a')[0]['href']
            # 괄호안 추출
            href = re.findall('\(([^)]+)', href)[0]
            temp['Id'] = str.replace(href.split(',')[1],"'","")
            temp['Si'] = tempSi
            # temp['type'] = 'congress'
            temp['District'] = tr.select('td')[0].text
            temp['Party'] = tr.select('td')[1].text
            temp['ImageUrl'] = 'http://info.nec.go.kr/'+ tr.select('td')[2].select('input')[0]['src']
            temp['Name'] = str.strip(tr.select('td')[3].text)
            temp['Gender'] = str.strip(tr.select('td')[4].text)
            temp['Age'] = tr.select('td')[5].text
            temp['Address'] = tr.select('td')[6].text
            temp['Job'] = tr.select('td')[7].text
            temp['Education'] = tr.select('td')[8].text
            temp['Career'] = tr.select('td')[9].text
            temp['Criminal'] = tr.select('td')[10].text
            temp['RegDate'] = str.strip(tr.select('td')[11].text)
            temp['Status'] = 'pre'

            print(temp)
            db.collection(u'congress').add(temp)

# 구·시·군의 장선거

driver.find_element_by_xpath('//*[@id="electionId4"]').click()
time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
cityOptions = soup.select('#cityCode > option')
cityCodes = [ o['value'] for o in cityOptions][1:]

for code in cityCodes:
    driver.find_element_by_xpath('//*[@id="cityCode"]').click()
    tempSi = driver.find_element_by_css_selector('#cityCode > [value="' + code + '"]').text
    driver.find_element_by_css_selector('#cityCode > [value="'+code+'"]').click()

    time.sleep(0.5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    sggCityOptions = soup.select('#sggCityCode > option')
    sggCityCodes = [o['value'] for o in sggCityOptions][1:]
    for sggCode in sggCityCodes:
        driver.find_element_by_xpath('//*[@id="sggCityCode"]').click()
        time.sleep(0.5)
        tempGu = driver.find_element_by_css_selector('#sggCityCode > [value="' + sggCode + '"]').text
        driver.find_element_by_css_selector('#sggCityCode > [value="' + sggCode + '"]').click()
        WebDriverWait(driver,15).until(EC.presence_of_element_located((By.ID, "spanSubmit"))).click()

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        resultTable = soup.select('#table01 > tbody > tr')

        for tr in resultTable:
            temp = dict()
            href = tr.select('td')[3].select('a')[0]['href']
            # 괄호안 추출
            href = re.findall('\(([^)]+)', href)[0]
            temp['Id'] = str.replace(href.split(',')[1],"'","")
            temp['Si'] = tempSi
            # temp['type'] = 'guMayor'
            temp['District'] = tr.select('td')[0].text
            temp['Party'] = tr.select('td')[1].text
            temp['ImageUrl'] = 'http://info.nec.go.kr/'+ tr.select('td')[2].select('input')[0]['src']
            temp['Name'] = str.strip(tr.select('td')[3].text)
            temp['Gender'] = str.strip(tr.select('td')[4].text)
            temp['Age'] = tr.select('td')[5].text
            temp['Address'] = tr.select('td')[6].text
            temp['Job'] = tr.select('td')[7].text
            temp['Education'] = tr.select('td')[8].text
            temp['Career'] = tr.select('td')[9].text
            temp['Criminal'] = tr.select('td')[10].text
            temp['RegDate'] = str.strip(tr.select('td')[11].text)
            temp['Status'] = 'pre'

            print(temp)
            db.collection(u'guMayor').add(temp)


# 시·도의회의원선거

driver.find_element_by_xpath('//*[@id="electionId5"]').click()
time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
cityOptions = soup.select('#cityCode > option')
cityCodes = [ o['value'] for o in cityOptions][1:]

for code in cityCodes:
    driver.find_element_by_xpath('//*[@id="cityCode"]').click()
    driver.find_element_by_css_selector('#cityCode > [value="'+code+'"]').click()
    tempSi = driver.find_element_by_css_selector('#cityCode > [value="'+code+'"]').text

    time.sleep(0.5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    townOptions = soup.select('#townCode > option')
    townCodes = [o['value'] for o in townOptions][1:]
    for townCode in townCodes:
        driver.find_element_by_xpath('//*[@id="townCode"]').click()
        time.sleep(0.5)
        tempGu = driver.find_element_by_css_selector('#townCode > [value="' + townCode + '"]').text
        driver.find_element_by_css_selector('#townCode > [value="' + townCode + '"]').click()

        time.sleep(0.5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        sggTownOptions = soup.select('#sggTownCode > option')
        sggTownCodes = [o['value'] for o in sggTownOptions][1:]
        for sggTown in sggTownCodes:
            driver.find_element_by_xpath('//*[@id="sggTownCode"]').click()
            time.sleep(0.5)
            driver.find_element_by_css_selector('#sggTownCode > [value="' + sggTown + '"]').click()
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "spanSubmit"))).click()

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            resultTable = soup.select('#table01 > tbody > tr')

            for tr in resultTable:
                temp = dict()
                href = tr.select('td')[3].select('a')[0]['href']
                # 괄호안 추출
                href = re.findall('\(([^)]+)', href)[0]
                temp['Id'] = str.replace(href.split(',')[1],"'","")
                temp['Si'] = tempSi
                temp['Gu'] = tempGu
                # temp['type'] = 'siCouncil'
                temp['District'] = tr.select('td')[0].text
                temp['Party'] = tr.select('td')[1].text
                temp['ImageUrl'] = 'http://info.nec.go.kr/'+ tr.select('td')[2].select('input')[0]['src']
                temp['Name'] = str.strip(tr.select('td')[3].text)
                temp['Gender'] = str.strip(tr.select('td')[4].text)
                temp['Age'] = tr.select('td')[5].text
                temp['Address'] = tr.select('td')[6].text
                temp['Job'] = tr.select('td')[7].text
                temp['Education'] = tr.select('td')[8].text
                temp['Career'] = tr.select('td')[9].text
                temp['Criminal'] = tr.select('td')[10].text
                temp['RegDate'] = str.strip(tr.select('td')[11].text)
                temp['Status'] = 'pre'

                print(temp)
                db.collection(u'siCouncil').add(temp)


# 구·시·군의회의원선거

driver.find_element_by_xpath('//*[@id="electionId6"]').click()
time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
cityOptions = soup.select('#cityCode > option')
cityCodes = [ o['value'] for o in cityOptions][1:]

for code in cityCodes:
    driver.find_element_by_xpath('//*[@id="cityCode"]').click()
    driver.find_element_by_css_selector('#cityCode > [value="'+code+'"]').click()
    tempSi = driver.find_element_by_css_selector('#cityCode > [value="'+code+'"]').text

    time.sleep(0.5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    townOptions = soup.select('#townCode > option')
    townCodes = [o['value'] for o in townOptions][1:]
    for townCode in townCodes:
        driver.find_element_by_xpath('//*[@id="townCode"]').click()
        time.sleep(0.5)
        tempGu = driver.find_element_by_css_selector('#townCode > [value="' + townCode + '"]').text
        driver.find_element_by_css_selector('#townCode > [value="' + townCode + '"]').click()

        time.sleep(0.5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        sggTownOptions = soup.select('#sggTownCode > option')
        sggTownCodes = [o['value'] for o in sggTownOptions][1:]
        for sggTown in sggTownCodes:
            driver.find_element_by_xpath('//*[@id="sggTownCode"]').click()
            time.sleep(0.5)
            driver.find_element_by_css_selector('#sggTownCode > [value="' + sggTown + '"]').click()
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "spanSubmit"))).click()

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            resultTable = soup.select('#table01 > tbody > tr')

            for tr in resultTable:
                temp = dict()
                if len(tr.select('td')) == 1:
                    continue
                href = tr.select('td')[3].select('a')[0]['href']
                # 괄호안 추출
                href = re.findall('\(([^)]+)', href)[0]
                temp['Id'] = str.replace(href.split(',')[1],"'","")
                temp['Si'] = tempSi
                temp['Gu'] = tempGu
                # temp['type'] = 'guCouncil'
                temp['District'] = tr.select('td')[0].text
                temp['Party'] = tr.select('td')[1].text
                temp['ImageUrl'] = 'http://info.nec.go.kr/'+ tr.select('td')[2].select('input')[0]['src']
                temp['Name'] = str.strip(tr.select('td')[3].text)
                temp['Gender'] = str.strip(tr.select('td')[4].text)
                temp['Age'] = tr.select('td')[5].text
                temp['Address'] = tr.select('td')[6].text
                temp['Job'] = tr.select('td')[7].text
                temp['Education'] = tr.select('td')[8].text
                temp['Career'] = tr.select('td')[9].text
                temp['Criminal'] = tr.select('td')[10].text
                temp['RegDate'] = str.strip(tr.select('td')[11].text)
                temp['Status'] = 'pre'

                print(temp)
                db.collection(u'guCouncil').add(temp)