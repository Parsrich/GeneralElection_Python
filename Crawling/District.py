import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

import time

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

## 국회의원 지역구

driver = webdriver.Chrome('/Users/kyome/dev/Parsrich/GeneralElection/python/Crawling/chromedriver')
driver.get("http://info.nec.go.kr/main/showDocument.xhtml?electionId=0020200415&topMenuId=BI&secondMenuId=BIGI05")
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

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "spanSubmit"))).click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    resultTable = soup.select('#table01 > tbody > tr')
    # print(resultTable)

    preElectionDistrictName = ''
    for tr in resultTable:
        temp = dict()
        temp['si'] = driver.find_element_by_css_selector('#cityCode > [value="'+code+'"]').text
        if len(tr.select('td')[0].contents) > 0 :
            temp['electionDistrictName'] = tr.select('td')[0].contents[0]
            preElectionDistrictName = temp['electionDistrictName']
        else :
            temp['electionDistrictName'] = preElectionDistrictName

        temp['gu'] = tr.select('td')[2].contents[0]

        tempDong = str.strip(tr.select('td')[3].contents[0]).split(', ')
        temp['dong'] = list()

        for dong in tempDong:

            # 괄호 안에 지역
            alterGu = ""

            # 괄호가 있으면
            if '(' in dong:
                alterGu = re.findall('\(([^)]+)', dong)[0]
                dong = re.sub(r'\([^)]*\)', '', dong)

            if '·' not in dong:
                if alterGu != "":
                    dong = dong + "_" + alterGu
                temp['dong'].append(dong)
            else:
                if '종로' in dong:
                    jongloSplit = dong.split('·')

                    pre = '종로'
                    post = '가동'

                    for idx,jonglo in enumerate(jongloSplit):
                        if idx == 0 :
                            jongloSplit[idx] = jonglo + post
                        elif idx == len(jongloSplit) - 1:
                            jongloSplit[idx] = pre + jonglo
                        else:
                            jongloSplit[idx] = pre + jonglo + post

                    temp['dong'].extend(jongloSplit)

                elif dong[len(dong)-2:] == '가동':
                    dongSplit = dong.split('·')
                    pre = dongSplit[0][:len(dongSplit[0]) - 1]
                    print(pre)
                    print(dongSplit )
                    for idx, d in enumerate(dongSplit):
                        if idx == 0:
                            dongSplit[idx] = d + '가동'
                        elif idx == len(dongSplit) - 1:
                            if dongSplit[idx][0].isdigit():
                                dongSplit[idx] = pre + d
                            else:
                                dongSplit[idx] = d

                        else:
                            if dongSplit[idx][-1].isdigit():
                                dongSplit[idx] = pre + d + '가동'
                            else:
                                dongSplit[idx] = d + '가동'
                        if alterGu != "":
                            dongSplit[idx] = dongSplit[idx] + "_" + alterGu
                    temp['dong'].extend(dongSplit)
                    print(dongSplit)
                else:
                    dongSplit = dong.split('·')
                    pre = dongSplit[0][:len(dongSplit[0]) - 1]
                    for idx, d in enumerate(dongSplit):
                        if idx == 0:
                            dongSplit[idx] = d + '동'
                        elif idx == len(dongSplit) - 1:
                            if dongSplit[idx][0].isdigit():
                                dongSplit[idx] = pre + d
                            else:
                                dongSplit[idx] = d

                        else:
                            if dongSplit[idx][-1].isdigit():
                                dongSplit[idx] = pre + d + '동'
                            else:
                                dongSplit[idx] = d + '동'
                        if alterGu != "":
                            dongSplit[idx] = dongSplit[idx] + "_" + alterGu
                    temp['dong'].extend(dongSplit)
        # print(temp)

        for d in temp['dong']:

            if '_' in d :
                temp['gu'] = d.split('_')[1]
                d = d.split('_')[0]

            doc_ref = db.collection(u'district').document()
            doc_ref.set({
                u'Si': temp['si'],
                u'Gu':temp['gu'],
                u'Dong': d,
                u'Congress': temp['electionDistrictName']
            })

            print({
                u'Si': temp['si'],
                u'Gu':temp['gu'],
                u'Dong': d,
                u'Congress': temp['electionDistrictName']
            })

## 구·시·군의 장선거
driver = webdriver.Chrome('/Users/kyome/dev/Parsrich/GeneralElection/python/Crawling/chromedriver')
driver.get("http://info.nec.go.kr/main/showDocument.xhtml?electionId=0020200415&topMenuId=BI&secondMenuId=BIGI05")
driver.maximize_window()
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="electionId4"]'))).click()
time.sleep(1)


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
cityOptions = soup.select('#cityCode > option')
cityCodes = [ o['value'] for o in cityOptions][1:]

for code in cityCodes:
    driver.find_element_by_xpath('//*[@id="cityCode"]').click()
    driver.find_element_by_css_selector('#cityCode > [value="'+code+'"]').click()

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "spanSubmit"))).click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    resultTable = soup.select('#table01 > tbody > tr')
    # print(resultTable)

    preElectionDistrictName = ''
    for tr in resultTable:
        temp = dict()
        temp['si'] = driver.find_element_by_css_selector('#cityCode > [value="'+code+'"]').text
        if len(tr.select('td')[0].contents) > 0 :
            temp['electionDistrictName'] = tr.select('td')[0].contents[0]
            preElectionDistrictName = temp['electionDistrictName']
        else :
            temp['electionDistrictName'] = preElectionDistrictName

        temp['gu'] = tr.select('td')[2].contents[0]

        tempDong = str.strip(tr.select('td')[3].contents[0]).split(', ')
        temp['dong'] = list()

        for dong in tempDong:

            # 괄호 안에 지역
            alterGu = ""

            # 괄호가 있으면
            if '(' in dong:
                alterGu = re.findall('\(([^)]+)', dong)[0]
                dong = re.sub(r'\([^)]*\)', '', dong)

            if '·' not in dong:
                if alterGu != "":
                    dong = dong + "_" + alterGu
                temp['dong'].append(dong)
            else:
                if '종로' in dong:
                    jongloSplit = dong.split('·')

                    pre = '종로'
                    post = '가동'

                    for idx,jonglo in enumerate(jongloSplit):
                        if idx == 0 :
                            jongloSplit[idx] = jonglo + post
                        elif idx == len(jongloSplit) - 1:
                            jongloSplit[idx] = pre + jonglo
                        else:
                            jongloSplit[idx] = pre + jonglo + post
                    temp['dong'].extend(jongloSplit)

                elif dong[len(dong)-2:] == '가동':
                    dongSplit = dong.split('·')
                    pre = dongSplit[0][:len(dongSplit[0]) - 1]
                    print(pre)
                    print(dongSplit )
                    for idx, d in enumerate(dongSplit):
                        if idx == 0:
                            dongSplit[idx] = d + '가동'
                        elif idx == len(dongSplit) - 1:
                            if dongSplit[idx][0].isdigit():
                                dongSplit[idx] = pre + d
                            else:
                                dongSplit[idx] = d

                        else:
                            if dongSplit[idx][-1].isdigit():
                                dongSplit[idx] = pre + d + '가동'
                            else:
                                dongSplit[idx] = d + '가동'
                        if alterGu != "":
                            dongSplit[idx] = dongSplit[idx] + "_" + alterGu
                    temp['dong'].extend(dongSplit)
                else:
                    dongSplit = dong.split('·')
                    pre = dongSplit[0][:len(dongSplit[0]) - 1]
                    for idx, d in enumerate(dongSplit):
                        if idx == 0:
                            dongSplit[idx] = d + '동'
                        elif idx == len(dongSplit) - 1:
                            if dongSplit[idx][0].isdigit():
                                dongSplit[idx] = pre + d
                            else:
                                dongSplit[idx] = d

                        else:
                            if dongSplit[idx][-1].isdigit():
                                dongSplit[idx] = pre + d + '동'
                            else:
                                dongSplit[idx] = d + '동'
                        if alterGu != "":
                            dongSplit[idx] = dongSplit[idx] + "_" + alterGu
                    temp['dong'].extend(dongSplit)
        # print(temp)

        for d in temp['dong']:

            if '_' in d :
                temp['gu'] = d.split('_')[1]
                d = d.split('_')[0]

            district_ref = db.collection(u'district')
            query_ref = district_ref.where(u'Si', u'==', temp['si']) \
                .where(u'Gu', u'==', temp['gu'])\
                .where(u'Dong', u'==', d)

            docs = query_ref.stream()
            for doc in docs:
                district_ref.document(doc.id).update({u'GuMayor': temp['electionDistrictName']})

# ## 시·도의회의원선거

# driver = webdriver.Chrome('/Users/kyome/dev/Parsrich/GeneralElection/python/Crawling/chromedriver')
driver.get("http://info.nec.go.kr/main/showDocument.xhtml?electionId=0020200415&topMenuId=BI&secondMenuId=BIGI05")
driver.maximize_window()
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="electionId5"]'))).click()
time.sleep(1)


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
cityOptions = soup.select('#cityCode > option')
cityCodes = [ o['value'] for o in cityOptions][1:]

for code in cityCodes:
    driver.find_element_by_xpath('//*[@id="cityCode"]').click()
    driver.find_element_by_css_selector('#cityCode > [value="'+code+'"]').click()

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "spanSubmit"))).click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    resultTable = soup.select('#table01 > tbody > tr')
    # print(resultTable)

    preElectionDistrictName = ''
    for tr in resultTable:
        temp = dict()
        temp['si'] = driver.find_element_by_css_selector('#cityCode > [value="'+code+'"]').text
        if len(tr.select('td')[1].contents) > 0 :
            temp['electionDistrictName'] = tr.select('td')[1].contents[0]
            preElectionDistrictName = temp['electionDistrictName']
        else :
            temp['electionDistrictName'] = preElectionDistrictName

        temp['gu'] = tr.select('td')[0].contents[0]

        tempDong = str.strip(tr.select('td')[3].contents[0]).split(', ')
        temp['dong'] = list()
        for dong in tempDong:
            # 괄호 안에 지역
            alterGu = ""

            # 괄호가 있으면
            if '(' in dong:
                alterGu = re.findall('\(([^)]+)', dong)[0]
                dong = re.sub(r'\([^)]*\)', '', dong)

            if '·' not in dong:
                if alterGu != "":
                    dong = dong + "_" + alterGu
                temp['dong'].append(dong)
            else:
                if '종로' in dong:
                    jongloSplit = dong.split('·')

                    pre = '종로'
                    post = '가동'

                    for idx,jonglo in enumerate(jongloSplit):
                        if idx == 0 :
                            jongloSplit[idx] = jonglo + post
                        elif idx == len(jongloSplit) - 1:
                            jongloSplit[idx] = pre + jonglo
                        else:
                            jongloSplit[idx] = pre + jonglo + post
                    temp['dong'].extend(jongloSplit)

                elif dong[len(dong)-2:] == '가동':
                    dongSplit = dong.split('·')
                    pre = dongSplit[0][:len(dongSplit[0]) - 1]
                    print(pre)
                    print(dongSplit )
                    for idx, d in enumerate(dongSplit):
                        if idx == 0:
                            dongSplit[idx] = d + '가동'
                        elif idx == len(dongSplit) - 1:
                            if dongSplit[idx][0].isdigit():
                                dongSplit[idx] = pre + d
                            else:
                                dongSplit[idx] = d

                        else:
                            if dongSplit[idx][-1].isdigit():
                                dongSplit[idx] = pre + d + '가동'
                            else:
                                dongSplit[idx] = d + '가동'
                        if alterGu != "":
                            dongSplit[idx] = dongSplit[idx] + "_" + alterGu
                    temp['dong'].extend(dongSplit)
                else:
                    dongSplit = dong.split('·')
                    pre = dongSplit[0][:len(dongSplit[0]) - 1]
                    for idx, d in enumerate(dongSplit):
                        if idx == 0:
                            dongSplit[idx] = d + '동'
                        elif idx == len(dongSplit) - 1:
                            if dongSplit[idx][0].isdigit():
                                dongSplit[idx] = pre + d
                            else:
                                dongSplit[idx] = d

                        else:
                            if dongSplit[idx][-1].isdigit():
                                dongSplit[idx] = pre + d + '동'
                            else:
                                dongSplit[idx] = d + '동'
                        if alterGu != "":
                            dongSplit[idx] = dongSplit[idx] + "_" + alterGu
                    temp['dong'].extend(dongSplit)
        # print(temp)

        for d in temp['dong']:

            if '_' in d :
                temp['gu'] = d.split('_')[1]
                d = d.split('_')[0]

            district_ref = db.collection(u'district')
            query_ref = district_ref.where(u'Si', u'==', temp['si']) \
                .where(u'Gu', u'==', temp['gu'])\
                .where(u'Dong', u'==', d)

            docs = query_ref.stream()
            for doc in docs:
                district_ref.document(doc.id).update({u'SiCouncil': temp['electionDistrictName']})


# ##구·시·군의회의원선거
# driver = webdriver.Chrome('/Users/kyome/dev/Parsrich/GeneralElection/python/Crawling/chromedriver')
driver.get("http://info.nec.go.kr/main/showDocument.xhtml?electionId=0020200415&topMenuId=BI&secondMenuId=BIGI05")
driver.maximize_window()
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="electionId6"]'))).click()
time.sleep(1)


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
cityOptions = soup.select('#cityCode > option')
cityCodes = [ o['value'] for o in cityOptions][1:]

for code in cityCodes:
    driver.find_element_by_xpath('//*[@id="cityCode"]').click()
    driver.find_element_by_css_selector('#cityCode > [value="'+code+'"]').click()

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "spanSubmit"))).click()

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    resultTable = soup.select('#table01 > tbody > tr')
    # print(resultTable)

    preElectionDistrictName = ''
    for tr in resultTable:
        temp = dict()
        temp['si'] = driver.find_element_by_css_selector('#cityCode > [value="'+code+'"]').text
        if len(tr.select('td')[1].contents) > 0 :
            temp['electionDistrictName'] = tr.select('td')[1].contents[0]
            preElectionDistrictName = temp['electionDistrictName']
        else :
            temp['electionDistrictName'] = preElectionDistrictName

        temp['gu'] = tr.select('td')[0].contents[0]

        tempDong = str.strip(tr.select('td')[3].contents[0]).split(', ')
        temp['dong'] = list()

        for dong in tempDong:
            # 괄호 안에 지역
            alterGu = ""

            # 괄호가 있으면
            if '(' in dong:
                alterGu = re.findall('\(([^)]+)', dong)[0]
                dong = re.sub(r'\([^)]*\)', '', dong)

            if '·' not in dong:
                if alterGu != "":
                    dong = dong + "_" + alterGu
                temp['dong'].append(dong)
            else:
                if '종로' in dong:
                    jongloSplit = dong.split('·')

                    pre = '종로'
                    post = '가동'

                    for idx,jonglo in enumerate(jongloSplit):
                        if idx == 0 :
                            jongloSplit[idx] = jonglo + post
                        elif idx == len(jongloSplit) - 1:
                            jongloSplit[idx] = pre + jonglo
                        else:
                            jongloSplit[idx] = pre + jonglo + post
                    temp['dong'].extend(jongloSplit)

                elif dong[len(dong)-2:] == '가동':
                    dongSplit = dong.split('·')
                    pre = dongSplit[0][:len(dongSplit[0]) - 1]
                    print(pre)
                    print(dongSplit )
                    for idx, d in enumerate(dongSplit):
                        if idx == 0:
                            dongSplit[idx] = d + '가동'
                        elif idx == len(dongSplit) - 1:
                            if dongSplit[idx][0].isdigit():
                                dongSplit[idx] = pre + d
                            else:
                                dongSplit[idx] = d

                        else:
                            if dongSplit[idx][-1].isdigit():
                                dongSplit[idx] = pre + d + '가동'
                            else:
                                dongSplit[idx] = d + '가동'
                        if alterGu != "":
                            dongSplit[idx] = dongSplit[idx] + "_" + alterGu
                    temp['dong'].extend(dongSplit)
                else:
                    dongSplit = dong.split('·')
                    pre = dongSplit[0][:len(dongSplit[0]) - 1]
                    for idx, d in enumerate(dongSplit):
                        if idx == 0:
                            dongSplit[idx] = d + '동'
                        elif idx == len(dongSplit) - 1:
                            if dongSplit[idx][0].isdigit():
                                dongSplit[idx] = pre + d
                            else:
                                dongSplit[idx] = d

                        else:
                            if dongSplit[idx][-1].isdigit():
                                dongSplit[idx] = pre + d + '동'
                            else:
                                dongSplit[idx] = d + '동'
                        if alterGu != "":
                            dongSplit[idx] = dongSplit[idx] + "_" + alterGu
                    temp['dong'].extend(dongSplit)
        # print(temp)

        for d in temp['dong']:

            if '_' in d :
                temp['gu'] = d.split('_')[1]
                d = d.split('_')[0]

            district_ref = db.collection(u'district')
            query_ref = district_ref.where(u'Si', u'==', temp['si']) \
                .where(u'Gu', u'==', temp['gu'])\
                .where(u'Dong', u'==', d)

            docs = query_ref.stream()
            for doc in docs:
                district_ref.document(doc.id).update({u'GuCouncil': temp['electionDistrictName']})


## 확인용 쿼리
district_ref = db.collection(u'district')
query_ref = district_ref.where(u'Si', u'==', u'대전광역시')

docs = query_ref.stream()
for doc in docs:
    print(doc.to_dict())
