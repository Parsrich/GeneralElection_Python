import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import re
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
#
# db = firestore.client()
#
# ## 확인용 쿼리
# district_ref = db.collection(u'district')
# query_ref = district_ref.where(u'Si', u'==', u'서울특별시').where(u'Gu',u'==',u'종로구').where(u'Dong',u'==',u'청운효자동')
#
# docs = query_ref.stream()
# for doc in docs:
#     print(doc.to_dict())


rexComple = re.compile('\([^)]*\)')

m = rexComple.match("python(aa)")

test = "pyth(ss)on(aa)"
print(re.findall('\(([^)]+)', test)[0])


remove_text = 'asdf(aㅁㅁㅁsdf)'
print(re.sub(r'\([^)]*\)', '', remove_text))
