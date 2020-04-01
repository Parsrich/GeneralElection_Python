import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import json
import copy

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
#
db = firestore.client()

candidate_ref = db.collection(u'district')

docs = candidate_ref.stream()
result = dict()
for doc in docs:
    temp = doc.to_dict()

    if temp['Si'] not in result.keys():
        result[temp['Si']] = dict()

    if  temp['Gu'] not in result[temp['Si']].keys():
        result[temp['Si']][temp['Gu']] = dict()

    if temp['Dong'] not in result[temp['Si']][temp['Gu']].keys():
        result[temp['Si']][temp['Gu']][temp['Dong']] = dict()

    t = {'congress': '','guMayor' : '', 'siCouncil' : '', 'guCouncil' : ''}


    if 'Congress' in temp.keys() :
        t['congress'] = temp['Congress']
    if 'GuMayor' in temp.keys():
        t['guMayor'] = temp['GuMayor']
    if 'SiCouncil' in temp.keys():
        t['siCouncil'] = temp['SiCouncil']
    if 'GuCouncil' in temp.keys():
        t['guCouncil'] = temp['GuCouncil']

    result[temp['Si']][temp['Gu']][temp['Dong']] = t

print(result)

with open("district.json", "w",encoding='UTF-8') as json_file:
    json.dump(result, json_file,ensure_ascii=False)

# with open("district_seoul.json", "w",encoding='UTF-8') as json_file:
#     json.dump(result['서울특별시'], json_file,ensure_ascii=False)
