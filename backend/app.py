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




app = Flask(__name__)
CORS(app)  # Allow CORS for all routes


@app.route('/due_Date_Matching', methods=['GET'])
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
    return jsonify({"message": "Due date matching completed successfully"})




if __name__ == '__main__':
    app.run(debug=True)