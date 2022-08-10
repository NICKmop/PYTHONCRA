import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

   
class firebase_con:
    cred = credentials.Certificate('D:/PYTHONCRA/crawling/dbbox/freecomponent-firebase-adminsdk-pdeca-4a9d5105f1.json')
    firebase_admin.initialize_app(cred,{ 'databaseURL' : 'https://freecomponent-default-rtdb.firebaseio.com/'});


    def updateModel(name,i,values):
        db = firestore.client();
        doc_ref = db.collection(u'crawlingData').document(name)
        doc_ref.update({"{}_{}".format(name,i) : values});

