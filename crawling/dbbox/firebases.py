import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

   
class firebase_con:
    cred = credentials.Certificate('D:/PYTHONCRA/crawling/dbbox/dbcurd-67641-firebase-adminsdk-ax50d-0e1098879e.json')
    firebase_admin.initialize_app(cred,{ 'databaseURL' : 'https://dbcurd-67641-default-rtdb.firebaseio.com/'});


    def updateModel(name,i,values):
        db = firestore.client();
        doc_ref = db.collection(u'crawlingData').document(name)
        doc_ref.update({"{}_{}".format(name,i) : values});

