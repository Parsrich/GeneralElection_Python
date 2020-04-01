import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import json
import copy

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
#
db = firestore.client()

candidate_ref = db.collection(u'Proportional')





docs = candidate_ref.stream()


result = dict()
name = dict()
for doc in docs:
    temp = doc.to_dict()

    if temp['Name'] not in list(name.keys()):
        name[temp['Name']] = list()

    name[temp['Name']].append(temp)

    # print(list(name.keys()))
candidate_ref = db.collection(u'guCouncil')
docs = candidate_ref.stream()
for doc in docs:
    temp = doc.to_dict()

    if temp['Name'] not in list(name.keys()):
        name[temp['Name']] = list()

    name[temp['Name']].append(temp)

candidate_ref = db.collection(u'siCouncil')
docs = candidate_ref.stream()
for doc in docs:
    temp = doc.to_dict()

    if temp['Name'] not in list(name.keys()):
        name[temp['Name']] = list()

    name[temp['Name']].append(temp)


candidate_ref = db.collection(u'guMayor')
docs = candidate_ref.stream()
for doc in docs:
    temp = doc.to_dict()

    if temp['Name'] not in list(name.keys()):
        name[temp['Name']] = list()

    name[temp['Name']].append(temp)



candidate_ref = db.collection(u'congress')
docs = candidate_ref.stream()
for doc in docs:
    temp = doc.to_dict()

    if temp['Name'] not in list(name.keys()):
        name[temp['Name']] = list()

    name[temp['Name']].append(temp)


#     if result.get(district) is None :
#         result[district] = list()
#     result[district].append(temp)
#
with open("name.json", "w",encoding='UTF-8') as json_file:
    json.dump(name, json_file,ensure_ascii=False)
