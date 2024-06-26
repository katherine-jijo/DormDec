import random
from copy import deepcopy
import pyrebase
from blockFunctionality import *
from roomAssignments import *

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

#Updates user data in the database to include data from the questionnaire
def saveStudentInfo():
    userList = db.child('users').get()
    for userData in userList:
        user = userData.val()
        
        #print(user)
        
        userID = user['userID']
        userQuestionnaire = db.child('studentQuestionnaireResponses').child(str(userID)).get().val()
        user['name'] = userQuestionnaire['user']['name']

        user['standing'] = userQuestionnaire['user']['classStanding']
        if (user['standing'] == 'Graduate/Law/Med'):
            user['standing'] = 'Graduate'
        #if
            
        user['gender'] = userQuestionnaire['user']['sex']
        if (user['gender'] not in ['Male', 'Female']):
            user['gender'] = userQuestionnaire['preferences']['roommateSex']
        #if

        user['roomType'] = userQuestionnaire['housing']['roomType']
        if (user['roomType'] == 'Single Room'):
            user['roomType'] = 'Single'
        elif (user['roomType'] == 'Double Room'):
            user['roomType'] = 'Double'
        elif (user['roomType'] == 'Triple Room'):
            user['roomType'] = 'Triple'
        elif (user['roomType'] == 'Quad Room'):
            user['roomType'] = 'Quad'
        #if/else

        userBuildingPreference = []

        if (user['standing'] != 'Graduate'):
            userBuildingPreference.append(userQuestionnaire['housing']['firstChoice'])
            userBuildingPreference.append(userQuestionnaire['housing']['secondChoice'])
            userBuildingPreference.append(userQuestionnaire['housing']['thirdChoice'])
        #if
        else:
            userBuildingPreference = ['Graduate', 'Graduate', 'Graduate']
        user['buildingPreference'] = userBuildingPreference
        #else
        
        if (('inBlock' not in user) or (user['inBlock'] == '')):
            user['inBlock'] = ''

        #if

        db.child('users').child(userData.key()).set(user)

    #for

#Orders all users into their appropriate selection pool.
def setSelectionPools():
    freshmenBuildings = ['Delft House', 'Groningen House', 'Hague House', 'Leiden House', 'Rotterdam House',            #These buildings only have 1 room type, so they only have 2 selection pools each
                         'Tilburg House', 'Urtrecht House', 'Orange House', 'Rensselaer House',
                     'Breukelen House', 'Amsterdam House', 'Stuyvesant Hall']
    
    saveStudentInfo()
    userList = db.child('users').get()
    
    for student in userList:
        gender = student.val()['gender']
        pool = student.val()['buildingPreference'][0]
        
        if ((pool in freshmenBuildings) == False):                                                                      #Not the freshmen buildings
            roomPreference = student.val()['roomType'] 
            studentArray = db.child('selectionPools').child(pool).child(gender).child(roomPreference).get().val()

            if ((studentArray is None) or (studentArray[0] is None) or (studentArray[0] == "")):
                studentArray = [student.key()]
            #if
            elif(student.key() not in studentArray):
                studentArray.append(student.key())
            #elif
            
            db.child('selectionPools').child(pool).child(gender).child(roomPreference).set(studentArray)
        #if
        
        else:                                                                                                           #freshmen buildings
            studentArray = db.child('selectionPools').child(pool).child(gender).get().val()

            if ((studentArray is None) or (studentArray[0] is None) or (studentArray[0] == "")):
                studentArray = [student.key()]
            #if
            elif(student.key() not in studentArray):
                studentArray.append(student.key())
            #elif
            
            db.child('selectionPools').child(pool).child(gender).set(studentArray)
        #else
    #for

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
    result = 0
    
    userQuestionnaire = db.child('studentQuestionnaireResponses').child(userId).get().val()
    otherQuestionnaire = db.child('studentQuestionnaireResponses').child(otherUserId).get().val()
    
    #Compare second and third building choices
    if (userQuestionnaire['housing']['secondChoice'] == otherQuestionnaire['housing']['secondChoice']):
        result += 1
        
    #if
        
    if (userQuestionnaire['housing']['thirdChoice'] == otherQuestionnaire['housing']['thirdChoice']):
        result += 1
        
    #if
    
    #Compare remaining preferences
    for preference in userQuestionnaire['preferences']:
        if ((userQuestionnaire['preferences'][preference] == otherQuestionnaire['preferences'][preference]) or (userQuestionnaire['preferences'][preference] == 'No Preference') or (otherQuestionnaire['preferences'][preference] == ' No Preference')):
            result += 1
            
        #if
    #for
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
            hofID = db.child('users').child(str(user)).child('userID').get().val()                              #User's hofID is used to store questionnaire answers
            #studentResponses = db.child('studentQuestionnaireResponses').child(str(hofID)).get().val()           #Not final/won't work until questionnaire stuff is done

            j = 0
            for otherUser in userArray:
                
                if ((otherUser == user) or (scoreArray[i][j] != -1)):                                           #No need to compare against people that have already been compared against or user's self
                    j += 1
                    continue
                
                result = compareLists(user, otherUser)
                scoreArray[i][j] = result
                scoreArray[j][i] = result
                
                j += 1
                #if

            userArrayCopy = deepcopy(userArray)
            quickSort(scoreArray[i], userArrayCopy, 0, len(scoreArray) - 1)

            scoreArray[i] = list(reversed(scoreArray[i]))
            userArrayCopy = list(reversed(userArrayCopy))
            scoreArray[i].pop()
            userArrayCopy.pop()
            

            data = {
                'scoreArray' : scoreArray[i],
                'topUserList' : userArrayCopy

            }
            db.child('preferenceLists').child(str(hofID)).set(data)                                             #Do not uncomment until questionnaire stuff is done

            i += 1

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

#Returns a given user's preference list
def getUserList(user):
    userID = db.child('users').child(str(user)).child('userID').get().val()
    return db.child('preferenceLists').child(str(userID)).child('topUserList').get().val()

#Fills new blocks created during dueDateMatching()
def fillBlock(roomType, blockID):
    if roomType == "Double":
        i = 2
    elif roomType == "Triple":
        i = 3
    elif roomType == "Quad":
        i = 4
    blockList = getBlockStudentList(str(blockID))
    if (blockList is not None):
        leader = blockList[0]
        leaderList = getUserList(leader)
        length = len(blockList)
        
        j = 0
        #print(length)
        #print(leaderList)
        if (leaderList is not None):
            while ((length < i) and (j < len(leaderList))):
                if (db.child('users').child(leaderList[j]).child('inBlock').get().val() == ''):
                    joinBlock(leaderList[j], blockID)
                    length += 1
                j += 1
                #if
            
            #while
        #if

#Automatically matches together all unassigned blocks to rooms and matches together all remaining students not in blocks
def dueDateMatching():
    blockList = getAllBlockList()
    #call room matching function                                                                            #Assign rooms to all pre-existing blocks
    assignAll()
    if (len(blockList) > 0):
        for block in blockList:
        
            db.child('blocks').child(block).remove()                                                                #Delete blocks after they are matched  #DONT UNCOMMENT UNTIL EVERYTHING IS DONE
        
    
    createPreferenceLists()
    userList = db.child('users').get()
    for user in userList:                                                                                       #Place remaining students into blocks
        student = user.val()
        
        print(student['name'])
        print(student['inBlock'])
        
        if (student['inBlock'] != ''):                                                                          #Students already in blocks are already accounted for
            continue
        #if
        
        createBlock(student['userData']['localId'])
        if student['roomType'] == 'Single':
            continue
        #if
        else:
            fillBlock(student['roomType'], student['userData']['localId'])                                      #Populate new block with users
        #else
    
        #call room matching function                                                                            #Match new block to rooms
        #db.child('blocks').child(student['userData']['localId']).remove()                                       #Delete the new block once matched to a room   #DONT UNCOMMENT UNTIL EVERYTHING IS DONE
    #for
    
    assignAll()
    blockList = getAllBlockList()
    for block in blockList:
        
        db.child('blocks').child(block).remove()
    
    printAllRooms()

#TO DO: Test setSelectionPools() by resetting Alliance Hall data - CHECK
#       Implement the student preference list algorithm - CHECK
#       Implement the final student matching algorithm - CHECK(ish)
#       Implement function to retrieve user's preference list as a sorted array of users in the same pool as them - CHECK
#       Implement function to save student info to database using info from questionnaires - CHECK

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

email = 'test+25@gmail.com'
password = '123456'
#user2 = auth.create_user_with_email_and_password(email2, pass2)
user = auth.create_user_with_email_and_password(email, password)
auth.user = None

data = {
  "userData" : {
      "email" : "test+25@gmail.com",
      "localId" : user['localId']
  },
  "userID": 200536279
}
db.child("users").child(user['localId']).set(data)
"""

#saveStudentInfo()