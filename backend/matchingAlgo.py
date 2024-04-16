import pyrebase
from blockFunctionality import *

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

freshmenBuildings = ['Delft House', 'Groningen House', 'Hague House', 'Leiden House', 'Rotterdam House', 'Tilburg House', 'Urtrecht House', 'Orange House', 'Rensselaer House',
                     'Breukelen House', 'Amsterdam House', 'Stuyvesant Hall']

#Orders all users into their appropriate selection pool
def setSelectionPools():
    userList = db.child('users').get()
    for student in userList:
        gender = student.val()['gender']
        pool = student.val()['buildingPreference'][0]
        
        if ((pool in freshmenBuildings) == False):                                                                      #Not the Nethies
            roomPreference = student.val()['roomType'] 
            studentArray = db.child('selectionPools').child(pool).child(gender).child(roomPreference).get().val()
            #print(studentArray)

            if ((studentArray is None) or (studentArray[0] is None)):
                studentArray = [student.key()]
            elif(student.key() not in studentArray):
                studentArray.append(student.key())

            db.child('selectionPools').child(pool).child(gender).child(roomPreference).set(studentArray)
        
        else:                                                                                                           #Nethies
            studentArray = db.child('selectionPools').child(pool).child(gender).get().val()

            if ((studentArray is None) or (studentArray[0] is None)):
                studentArray = [student.key()]
            elif(student.key() not in studentArray):
                studentArray.append(student.key())

            db.child('selectionPools').child(pool).child(gender).set(studentArray)


#setSelectionPools()

#TO DO: Test setSelectionPools() by resetting Alliance Hall data
#       Implement the student preference list algorithm
#       Implement the final student matching algorithm

#INITIALIZE SELECTION POOLS
"""buildingList = {'Delft House', 'Groningen House', 'Hague House', 'Leiden House', 'Rotterdam House',
                 'Tilburg House', 'Urtrecht House', 'Orange House', 'Rensselaer House', 'Breukelen House',
                 'Amsterdam House', 'Stuyvesant Hall', 'Alliance Hall', 'Bill of Rights Hall', 'Constitution Hall',
                   'Enterprise Hall', 'Estabrook Hall', 'Cambridge House', 'Dover House', 'Hampton House', 'Hempstead House', 'Jamestown House',
                   'New York House', 'Newport House', 'Plymouth House', 'Portsmouth House', 'Providence House',
                   'Quincy House', 'Suffolk Hall', 'Graduate'}"""

"""
buildingList = ['Suffolk Hall']
for building in buildingList:
    genderPools = {"Male" : {
        "Single" : [""],
        "Triple" : [""]
    },
                   "Female" : {
        "Single" : [""],
        "Triple" : [""]
    }}

    db.child('selectionPools').child(building).set(genderPools)"""