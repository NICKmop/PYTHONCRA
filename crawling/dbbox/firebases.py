from typing import Type
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

class firebase_con:
    current_working_directory = os.getcwd();
    cred = credentials.Certificate(current_working_directory+'/dbbox/dbcurd-67641-firebase-adminsdk-ax50d-0e1098879e.json')
    # cred = credentials.Certificate('/pythoncra/crawling/dbbox/dbcurd-67641-firebase-adminsdk-ax50d-0e1098879e.json')
    firebase_admin.initialize_app(cred,{ 'databaseURL' : 'https://dbcurd-67641-default-rtdb.firebaseio.com/'});

    def updateModel(name,i,values):
        db = firestore.client();
        # db.collection(u'crawlingData').document(name).delete();
        doc_ref = db.collection(u'crawlingData').document(name)
        doc_ref.update({"{}_{}".format(name,i) : values});
        
    def selectModelKeyNumber(name):
        spdataList = [];
        db = firestore.client();
        doc_ref = db.collection(u'crawlingData').document(name);
        doc = doc_ref.get();
        if doc.exists:
            originData = doc.to_dict().keys();
            for i in originData:
                if len(i.split("_")) == 3:
                    spdataList.append(int(i.split("_")[2]));
                
                if len(i.split("_")) == 2:
                    spdataList.append(int(i.split("_")[1]));
            return spdataList;
        else:
            print(u'No such document!')

    def selectModelValueNumber(name):
        spdataList = [];
        spdataDateList = [];
        db = firestore.client();
        doc_ref = db.collection(u'crawlingData').document(name);
        doc = doc_ref.get();
        if doc.exists:
            originData = doc.to_dict().values();
            for i in originData:
                spdataList.append(i['title'].strip());
                # spdataDateList.append(i['registrationdate']);

            return spdataList;
            # return spdataList,spdataDateList;
        else:
            print(u'No such document!')        

