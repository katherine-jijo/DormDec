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

#Orders all users into their appropriate selection pool.
def setSelectionPools():
    freshmenBuildings = ['Delft House', 'Groningen House', 'Hague House', 'Leiden House', 'Rotterdam House',    #These buildings only have 1 room type, so they only have 2 selection pools each
                         'Tilburg House', 'Urtrecht House', 'Orange House', 'Rensselaer House',
                     'Breukelen House', 'Amsterdam House', 'Stuyvesant Hall']
    
    userList = db.child('users').get()
    
    for student in userList:
        gender = student.val()['gender']
        pool = student.val()['buildingPreference'][0]
        
        if ((pool in freshmenBuildings) == False):                                                                      #Not the freshmen buildings
            roomPreference = student.val()['roomType'] 
            studentArray = db.child('selectionPools').child(pool).child(gender).child(roomPreference).get().val()
            #print(studentArray)

            if ((studentArray is None) or (studentArray[0] is None) or (studentArray[0] == "")):
                studentArray = [student.key()]
            elif(student.key() not in studentArray):
                studentArray.append(student.key())

            db.child('selectionPools').child(pool).child(gender).child(roomPreference).set(studentArray)
        
        else:                                                                                                           #freshmen buildings
            studentArray = db.child('selectionPools').child(pool).child(gender).get().val()

            if ((studentArray is None) or (studentArray[0] is None) or (studentArray[0] == "")):
                studentArray = [student.key()]
            elif(student.key() not in studentArray):
                studentArray.append(student.key())

            db.child('selectionPools').child(pool).child(gender).set(studentArray)


#setSelectionPools()

#TO DO: Test setSelectionPools() by resetting Alliance Hall data - CHECK
#       Implement the student preference list algorithm - WIP
#       Implement the final student matching algorithm
#       Implement function to retrieve user's preference list as a sorted array of users in the same pool as them

#Compares the questionnaire answers between each possible pair of users in a selection pool.
def compareLists(user, otherUser):
    userId = db.child('users').child(str(user)).child('userID').get().val()
    otherUserId = db.child('users').child(str(otherUser)).child('userID').get().val()
    pass
    return 1

#Creates the score lists for the users in a selection pool.
def createScoreLists(selectionPool):
    pool = selectionPool.val()
    if (pool[0] != ''):
        #pool = selectionPool

        #print(pool)
        #print(i)
        #scoreMatrix = {(i,j) : [] for i in range(10) for j in range(10)}
        #print(scoreMatrix)
        #print(pool)
    
        #Idea: make an array of all users in a pool, each index being itself assigned another array of all users in the pool
        #It's a little crude but it's the fastest to implement solution and we got like 5 days left so lets do this!
        userArray = []
        for user in pool:                                                       #Set up 2D array of users in selection pool
            userArray.append(user)

            #scoreMatrix = [][]
            pass
        
        #for

        scoreArray = []
        for i in range(len(userArray)):
            col = []
            for j in range(len(userArray)):
                col.append(-1)
            #for
            
            scoreArray.append(col)
            
        #for

        #print(scoreArray)
        #if ((pool is not None) or (pool[0] is not None) or (pool[0] != '')):    #Comparing lists
        #print(type(pool))
        i = 0
        for user in userArray:
            #print(user)
            #print(userArray.index(user))
            hofID = db.child('users').child(str(user)).child('userID').get().val()                              #User's hofID is used to store questionnaire answers
            #studentResponses = db.child('studentQuestionnaireResponses').child(str(hofID)).get().val()         #Not final/won't work until questionnaire stuff is done

            j = 0
            #insert for loop here
            for otherUser in userArray:
                if ((otherUser == user) or (scoreArray[i][j] != -1)):                                           #No need to compare against people that have already been compared against or user's self
                    j = j + 1
                    continue
                result = compareLists(user, otherUser)
                scoreArray[i][j] = result
                scoreArray[j][i] = result
                
                j = j + 1
                #if

            i = i + 1
            #call modified quicksort here
            #for

        #for
        pass
    
    #if

#Creates a preference list for every user in every selection pool.
#The lists for each user is limited to the same selection pool the user is in.
def createPreferenceLists():
    freshmenBuildings = ['Delft House', 'Groningen House', 'Hague House', 'Leiden House', 'Rotterdam House', 'Tilburg House', 'Urtrecht House', 'Orange House', 'Rensselaer House',
                     'Breukelen House', 'Amsterdam House', 'Stuyvesant Hall']
    setSelectionPools()
    selectionPools = db.child('selectionPools').get()
    #i = 0
    for building in selectionPools:
        for gender in building.val():
            if building.key() not in freshmenBuildings:
                poolList = db.child('selectionPools').child(building.key()).child(gender).get()
                
                for roomType in poolList:
                    #print(poolList)
                    #print(roomType.val())
                    #print(building.key())   
                    #print(gender)
                    createScoreLists(roomType)
                    #i += 1
                    #print(i)
                    #print("hi")
                
                
            else:
                pool = db.child('selectionPools').child(building.key()).child(gender).get()
                
                #print(pool.val())
                #print(building.key())
                #print(gender)
                createScoreLists(pool)
                #i += 1
                #print(i)
                
    
    return 0

testPool = db.child('selectionPools').child('Alliance Hall').child('Male').child('Double').get()
createScoreLists(testPool)
#createPreferenceLists()






#INITIALIZE SELECTION POOLS
"""buildingList = {'Delft House', 'Groningen House', 'Hague House', 'Leiden House', 'Rotterdam House',
                 'Tilburg House', 'Urtrecht House', 'Orange House', 'Rensselaer House', 'Breukelen House',
                 'Amsterdam House', 'Stuyvesant Hall', 'Alliance Hall', 'Bill of Rights Hall', 'Constitution Hall',
                   'Enterprise Hall', 'Estabrook Hall', 'Cambridge House', 'Dover House', 'Hampton House', 'Hempstead House', 'Jamestown House',
                   'New York House', 'Newport House', 'Plymouth House', 'Portsmouth House', 'Providence House',
                   'Quincy House', 'Suffolk Hall', 'Graduate'}"""

"""
buildingList = ['Cambridge House', 'Dover House', 'Hampton House', 'Hempstead House', 'Jamestown House',
                   'New York House', 'Newport House', 'Plymouth House', 'Portsmouth House', 'Providence House',
                   'Quincy House', 'Suffolk Hall']
for building in buildingList:
    genderPools = {"Male" : {
                        'Single' : [''],
                        'Triple' : ['']
                        },
        
                   "Female" : {
                       'Single' : [''],
                       'Triple' : ['']
                       }
    }

    db.child('selectionPools').child(building).set(genderPools)
"""

"""
###### FOR TESTING PURPOSES #######
auth = firebase.auth()

email = 'test+19@gmail.com'
password = '123456'
#user2 = auth.create_user_with_email_and_password(email2, pass2)
user = auth.create_user_with_email_and_password(email, password)
auth.user = None
data = {
  "name": "Avatar Korra",
  "gender" : "Female",
  "inBlock" : "",
  "roomType" : "Double",
  "standing": "Senior",
  "buildingPreference" : ['Alliance Hall', 'Enterprise Hall', 'Estabrook Hall'],
  "userData" : {
      "email" : "test+19@gmail.com",
      "localId" : user['localId']
  },
  "userID": 200420142
}
db.child("users").child(user['localId']).set(data)
"""