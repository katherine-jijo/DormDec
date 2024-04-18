import random
from copy import deepcopy
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
    freshmenBuildings = ['Delft House', 'Groningen House', 'Hague House', 'Leiden House', 'Rotterdam House',            #These buildings only have 1 room type, so they only have 2 selection pools each
                         'Tilburg House', 'Urtrecht House', 'Orange House', 'Rensselaer House',
                     'Breukelen House', 'Amsterdam House', 'Stuyvesant Hall']
    
    userList = db.child('users').get()
    
    for student in userList:
        gender = student.val()['gender']
        pool = student.val()['buildingPreference'][0]
        
        if ((pool in freshmenBuildings) == False):                                                                      #Not the freshmen buildings
            roomPreference = student.val()['roomType'] 
            studentArray = db.child('selectionPools').child(pool).child(gender).child(roomPreference).get().val()

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

######################################## QUICK SORT ##########################################

# Function to find the partition position
def partition(scoreArray, userArrayCopy, low, high):

    # Choose the rightmost element as pivot
    pivot = scoreArray[high]

    # Pointer for greater element
    i = low - 1

    # Traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if scoreArray[j] <= pivot:

            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1

            # Swapping element at i with element at j
            (scoreArray[i], scoreArray[j]) = (scoreArray[j], scoreArray[i])
            (userArrayCopy[i], userArrayCopy[j]) = (userArrayCopy[j], userArrayCopy[i])
        #if

    # Swap the pivot element with
    # the greater element specified by i
    (scoreArray[i + 1], scoreArray[high]) = (scoreArray[high], scoreArray[i + 1])
    (userArrayCopy[i + 1], userArrayCopy[high]) = (userArrayCopy[high], userArrayCopy[i + 1])
    #for

    # Return the position from where partition is done
    return i + 1

#A modified quicksort
def quickSort(scoreArray, userArrayCopy, low, high):
    if low < high:

        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pivot = partition(scoreArray, userArrayCopy, low, high)

        # Recursive call on the left of pivot
        quickSort(scoreArray, userArrayCopy, low, pivot - 1)

        # Recursive call on the right of pivot
        quickSort(scoreArray, userArrayCopy, pivot + 1, high)
    #if
    
######################################## QUICK SORT ##########################################

#Compares the questionnaire answers between each possible pair of users in a selection pool.
def compareLists(user, otherUser):
    userId = db.child('users').child(str(user)).child('userID').get().val()
    otherUserId = db.child('users').child(str(otherUser)).child('userID').get().val()

    # INSERT COMPARISON CODE HERE

    result = random.randint(1, 101)
    return result

#Creates the score lists for the users in a selection pool.
def createScoreLists(selectionPool):
    pool = selectionPool.val()
    if (pool[0] != ''):
        userArray = []
        
        for user in pool:                                                                                       #Set up 2D array of users in selection pool
            userArray.append(user)
        
        #for

        scoreArray = []
        for i in range(len(userArray)):
            col = []
            for j in range(len(userArray)):
                col.append(-1)
                
            #for
            scoreArray.append(col)
            
        #for
        
        i = 0
        for user in userArray:
            #hofID = db.child('users').child(str(user)).child('userID').get().val()                              #User's hofID is used to store questionnaire answers
            #studentResponses = db.child('studentQuestionnaireResponses').child(str(hofID)).get().val()           #Not final/won't work until questionnaire stuff is done

            j = 0
            for otherUser in userArray:
                
                if ((otherUser == user) or (scoreArray[i][j] != -1)):                                           #No need to compare against people that have already been compared against or user's self
                    j = j + 1
                    continue
                
                result = compareLists(user, otherUser)
                scoreArray[i][j] = result
                scoreArray[j][i] = result
                
                j = j + 1
                #if

            userArrayCopy = deepcopy(userArray)
            quickSort(scoreArray[i], userArrayCopy, 0, len(scoreArray) - 1)

            scoreArray[i] = list(reversed(scoreArray[i]))
            userArrayCopy = list(reversed(userArrayCopy))
            #scoreArray.pop()
            userArrayCopy.pop()
            

            data = {
                'scoreArray' : scoreArray[i],
                'topUserList' : userArrayCopy

            }
            #db.child('preferenceLists').child(str(hofID)).set(data)                                             #Do not uncomment until questionnaire stuff is done

            """
            print(user + ", USER " + str(db.child('users').child(user).child('name').get().val()) + " PRIORITY LIST")
            print(userArrayCopy)
            print(scoreArray[i])
            print("\n")
            """

            i = i + 1

            #for

        #for
    
    #if

#Creates a preference list for every user in every selection pool.
#The lists for each user is limited to the same selection pool the user is in.
def createPreferenceLists():
    freshmenBuildings = ['Delft House', 'Groningen House', 'Hague House', 'Leiden House', 'Rotterdam House', 'Tilburg House', 'Urtrecht House', 'Orange House', 'Rensselaer House',
                     'Breukelen House', 'Amsterdam House', 'Stuyvesant Hall']
    setSelectionPools()
    selectionPools = db.child('selectionPools').get()
    
    for building in selectionPools:
        for gender in building.val():
            if building.key() not in freshmenBuildings:
                poolList = db.child('selectionPools').child(building.key()).child(gender).get()
                
                for roomType in poolList:
                    createScoreLists(roomType)
                    
                
            else:
                pool = db.child('selectionPools').child(building.key()).child(gender).get()
                
                createScoreLists(pool)
    
    #return 0

testPool = db.child('selectionPools').child('Alliance Hall').child('Male').child('Double').get()

def dueDateMatching():
    pass

createScoreLists(testPool)
#createPreferenceLists()

#TO DO: Test setSelectionPools() by resetting Alliance Hall data - CHECK
#       Implement the student preference list algorithm - CHECK(ish)
#       Implement the final student matching algorithm
#       Implement function to retrieve user's preference list as a sorted array of users in the same pool as them




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