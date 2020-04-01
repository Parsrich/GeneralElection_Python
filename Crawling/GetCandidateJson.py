import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import json

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
#
db = firestore.client()

# candidate_ref = db.collection(u'congress')
#
# docs = candidate_ref.stream()

# result = dict()
# for doc in docs:
#     temp = doc.to_dict()
#     district = temp['Si'] +"_"+ temp['District']
#
#     if result.get(district) is None :
#         result[district] = list()
#     result[district].append(temp)
#
# with open("congress.json", "w",encoding='UTF-8') as json_file:
#     json.dump(result, json_file,ensure_ascii=False)
#
#
# # 구청장
#
# candidate_ref = db.collection(u'guMayor')
#
# docs = candidate_ref.stream()
#
#
# result = dict()
# for doc in docs:
#     temp = doc.to_dict()
#     district = temp['Si'] +"_"+ temp['District']
#
#     if result.get(district) is None :
#         result[district] = list()
#     result[district].append(temp)
#
# with open("guMayor.json", "w",encoding='UTF-8') as json_file:
#     json.dump(result, json_file,ensure_ascii=False)
#
# # 시의원
#
# candidate_ref = db.collection(u'siCouncil')
#
# docs = candidate_ref.stream()
#
#
# result = dict()
# for doc in docs:
#     temp = doc.to_dict()
#     district = temp['Si'] +"_"+ temp['District']
#
#     if result.get(district) is None :
#         result[district] = list()
#     result[district].append(temp)
#
# with open("siCouncil.json", "w",encoding='UTF-8') as json_file:
#     json.dump(result, json_file,ensure_ascii=False)
#
# # 구의원
#
# candidate_ref = db.collection(u'guCouncil')
#
# docs = candidate_ref.stream()
#
#
# result = dict()
# for doc in docs:
#     temp = doc.to_dict()
#     district = temp['Si'] +"_"+ temp['District']
#
#     if result.get(district) is None :
#         result[district] = list()
#     result[district].append(temp)
#
# with open("guCouncil.json", "w",encoding='UTF-8') as json_file:
#     json.dump(result, json_file,ensure_ascii=False)
#
# 구의원

candidate_ref = db.collection(u'Proportional')

docs = candidate_ref.stream()


result = dict()
for doc in docs:
    temp = doc.to_dict()
    district = temp['Party']

    if result.get(district) is None :
        result[district] = list()
    result[district].append(temp)

with open("proportional.json", "w",encoding='UTF-8') as json_file:
    json.dump(result, json_file,ensure_ascii=False)
