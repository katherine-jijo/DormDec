import pyrebase
#import time

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

"""
########################################################
#FOR TESTING PURPOSES
auth = firebase.auth()
testUser = auth.sign_in_with_email_and_password('test@gmail.com', '123456')
testUser2 = auth.sign_in_with_email_and_password('test+1@gmail.com', '123456')
#FOR TESTING PURPOSES
########################################################
"""

#Block management methods

def createBlock(userID):
    if (db.child('users').child(str(userID)).child('inBlock').get().val() == ''):
      userInfo = db.child('users').child(str(userID)).get().val()
      userName = db.child('users').child(str(userID)).child('name').get().val()
      data = {
      'Block Leader': userName,
      'Students in Block' : [userID],
      'Building' : userInfo['buildingPreference'][0]
      }
      db.child('blocks').child(str(userID)).set(data)
      db.child('users').child(str(userID)).child('inBlock').set(str(userID))#Add code to update user's data to say they are in this block

    else:
        if(str(userID) == db.child('users').child(str(userID)).child('inBlock').get().val()):
         print("Block already created")
        else:
           
         #print(userID)
         print("User is already in a block; can't create block")


#Initialize block method

def joinBlock(userID, leaderID):
    if (db.child('users').child(str(userID)).child('inBlock').get().val() == ''):
      blockList = db.child('blocks').child(str(leaderID)).child('Students in Block').get().val()
      #print(blockList)
      blockList.append(str(userID))
      db.child('blocks').child(str(leaderID)).child('Students in Block').set(blockList)
      db.child('users').child(str(userID)).child('inBlock').set(str(leaderID))

    else:
       raise Exception('User is already in a block')

#Allows a user to join a block with a block leader's ID

def leaveBlock(userID):
    leaderID = db.child('users').child(str(userID)).child('inBlock').get().val()
    if (leaderID != ''):
      blockList = db.child('blocks').child(str(leaderID)).child('Students in Block').get().val()
      blockList.remove(str(userID))
      db.child('blocks').child(str(leaderID)).child('Students in Block').set(blockList)
      db.child('users').child(str(userID)).child('inBlock').set('')

      if (len(blockList) == 0):
         db.child('blocks').child(str(leaderID)).remove()
      #Remove block from database if it is empty

      elif (leaderID == str(userID)):
         #remainingStudentList = db.child('blocks').child(str(leaderID)).child('Students in Block').get().val()
         newLeader = blockList[0]
         db.child('users').child(newLeader).child('inBlock').set('')
         createBlock(newLeader)

         for student in blockList:
            if (student == newLeader):
               continue
            else:
               #otherUserData = db.child('users').child(student).child('userData').get().val()
               db.child('users').child(student).child('inBlock').set('')
               #joinBlock(otherUserData, newLeader)
               joinBlock(student, newLeader)
         db.child('blocks').child(str(leaderID)).remove() 
      #Change block leader to remaining user who has been in the block the longest

    else:
       raise Exception('User is not in a block')

#Allows a user to leave a block they are in

def getBlockStudentList(blockID):
   return db.child('blocks').child(str(blockID)).child('Students in Block').get().val()

#Returns list of students in a block

def getAllBlockList():
   blockArray = []
   blockList = db.child('blocks').get()
   #print(blockList.val())
   if (blockList.val() is not None):
      for block in blockList.each():
         blockArray.append(block.key())
   
   return blockArray

#Returns array of all block keys in the database

"""
##############################################################
#TEST
#createBlock(testUser['localId'])
#joinBlock(testUser2['localId'], testUser['localId'])
#leaveBlock(testUser2['localId'])
#leaveBlock(testUser['localId'])
#print(getBlockStudentList('Fio73dgxyfcroMf4z7XIQYrUEiv1'))
#print(getAllBlockList())
##############################################################
"""
