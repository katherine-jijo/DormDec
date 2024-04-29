from flask import Flask, jsonify
from matchingAlgo import dueDateMatching
from matchingAlgo import getAllBlockList
from matchingAlgo import assignAll
from matchingAlgo import createPreferenceLists
from matchingAlgo import createBlock
from matchingAlgo import fillBlock
from matchingAlgo import db
from collections.abc import MutableMapping
import pyrebase
import collections
from flask_cors import CORS
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


app = Flask(__name__)
CORS(app)  # Allow CORS for all routes



@app.route('/dueDateMatching', methods=['GET'])
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
    
    """
    matching_results = []  # This should contain the actual matching results
    # Prepare matching results
    matching_results = []
    for user in userList:
        student = user.val()
        
        if student['inBlock'] == '':
            matching_results.append({"id": student['userData']['localId'], "name": student['name']})
            """
        

    #return jsonify({"message": "Due date matching completed successfully", "matching_results": matching_results})

    return jsonify({"message": "Due date matching completed successfully"})



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
