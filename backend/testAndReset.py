from matchingAlgo import *
from blockFunctionality import *
from roomAssignments import *
import pyrebase

firebaseConfig={'apiKey': "AIzaSyBZ_Nnybektn1URt1xv-A6_FTnLJs1adzQ",
  'authDomain': "dorm-deciders.firebaseapp.com",
  'projectId': "dorm-deciders",
  'storageBucket': "dorm-deciders.appspot.com",
  'messagingSenderId': "908311322524",
  'appId': "1:908311322524:web:8d53c41f9b42667a8fb259",
  'measurementId': "G-V8BYWBGHE6",
  'databaseURL': "https://dorm-deciders-default-rtdb.firebaseio.com/"}

firebase=pyrebase.initialize_app(firebaseConfig) #Initializes the firebase app

db = firebase.database()


#dueDateMatching()

#createBlock('Fio73dgxyfcroMf4z7XIQYrUEiv1')
#joinBlock('loFmInurgyarrZD5dg33RSj1jwT2', 'Fio73dgxyfcroMf4z7XIQYrUEiv1')



buildingList = db.child('buildings').get()
for building in buildingList.each():
    for roomType in building.val():
        for i in range(101, 400):
            if (roomType == 'Doubles') and (i % 10 == 2):
                db.child('buildings').child(building.key()).child(roomType).child(str(i)).set('')
            elif (roomType == 'Quads') and (i % 10 == 4):
                db.child('buildings').child(building.key()).child(roomType).child(str(i)).set('')
            elif (roomType == 'Singles') and (i % 10 == 1):
                db.child('buildings').child(building.key()).child(roomType).child(str(i)).set('')
            elif (roomType == 'Triples') and (i % 10 == 3):
                db.child('buildings').child(building.key()).child(roomType).child(str(i)).set('')

userList = db.child('users').get()
for user in userList:
    userID = user.key()
    db.child('users').child(userID).child('inBlock').set('')
    db.child('users').child(userID).child('roomAssignment').set('')

