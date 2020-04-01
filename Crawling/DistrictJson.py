# import firebase_admin
# from firebase_admin import firestore
# from firebase_admin import credentials
import copy
#
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
#
# db = firestore.client()
#
#
# # location_ref = db.collection(u'location')
#
# district_ref = db.collection(u'district')
# # query_ref = district_ref.where(u'Si', u'==', u'대전광역시')
#
# docs = district_ref.stream()
# # print(list(docs))
#
# SiGu = dict()
# GuDong = dict()
# for doc in docs:
#     temp = doc.to_dict()
#     print(temp)
#     if SiGu.get(temp['Si']) is None:
#         SiGu[temp['Si']] = set()
#         SiGu[temp['Si']].add(temp['Gu'])
#     else:
#         SiGu.get(temp['Si']).add(temp['Gu'])
#
#     SiGuName = (temp['Si'] + '_' + temp['Gu'])
#     if GuDong.get(SiGuName) is None:
#         GuDong[SiGuName] = set()
#         GuDong[SiGuName].add(temp['Dong'])
#     else:
#         GuDong.get(SiGuName).add(temp['Dong'])
#
#
# print(SiGu)
# for Si in SiGu:
#     print(Si)
#     print(list(SiGu[Si]))
#     db.collection(u'sigu').document(Si).set({'Gu': list(SiGu[Si])})
#
# print(GuDong)
# for Gu in GuDong:
#     print(Gu)
#     print(list(GuDong[Gu]))
#     db.collection(u'GuDong').document(Gu).set({'Dong': list(GuDong[Gu])})
#
# district_ref = db.collection(u'sigu')
# docs = district_ref.stream()
# temp = list()
# result=dict()
# for doc in docs:
#     docDict = doc.to_dict()
#     si = doc.id
#     result[si] = docDict['Gu']
#
# print(result)
#
# district_ref = db.collection(u'GuDong')
# docs = district_ref.stream()
# temp = list()
# result=dict()
# for doc in docs:
#
#     docDict = doc.to_dict()
#     sigu = doc.id
#     result[sigu] = docDict['Dong']
#
# print(result)


