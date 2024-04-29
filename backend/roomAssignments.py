"""
This file is used to take the blocks found in the Dorm Deciders firebase and
assign them to unfilled rooms in a different section of the firebase. To do
this, each block is evaluated for its subbin, aligned with a room based on a
FIFO system (first applicable room), and the block is assigned to that room by
assigning the room to the block and the block to the room. Written by Sam Rork
with assistance from Jonatan Salmeron in terms of the firebase setup logic.
"""

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

def assignment(blockID, building, size, room):
  """Assigns the userIDs in a block to a specific room.

  Only to be used internally, this function takes iterates through users in a 
  block defined by blockID and copies them under the room in the database.

  Args:
    blockID: the unique ID for the block which is to be assigned to this room.
      This ID is defined by the userID of whoever creates the block.
    building: a string defining which building subpool this block is to be
      assigned to.
    size: "Singles", "Doubles", "Triples", or "Quads", describes how many
      students will be in the room.
    room: the room number of the final room to be assigned to.
  
    Returns:
      True if the task completed successfully
    
    Raises:
  
  """
  try:
    block_users = db.child('blocks').child(str(blockID)).child('Students in Block').get()
    for user in block_users.each():
      if(user == block_users.each()[0]): # first child must be a "set" while adding children is "update"
        db.child('buildings').child(str(building)).child(str(size)).child(str(room)).set({user.key(): user.val()}) # make a new child labeled by the index and set it to the userID
      else:
        db.child('buildings').child(str(building)).child(str(size)).child(str(room)).update({user.key(): user.val()})
      db.child('users').child(str(user.val())).update({"roomAssignment": str(building) + " " + str(room)})
    return True
  except:
    print("An error occurred: invalid arguments")
    return False

def findAvailableRooms(building, size):
  """Creates a list of all rooms which fit the given criteria.

  Only to be used internally, this function takes iterates through the rooms
  which fit the criteria and adds them to a list if they are empty already.

  Args:
    building: a string defining which building subpool this block is to be
      assigned to.
    size: "Singles", "Doubles", "Triples", or "Quads", describes how many
      students will be in the room.
  
    Returns:
      a list (roomsList) which holds all the room numbers which fit the
        criteria and are empty.
    
    Raises:
  
  """
  try:
    roomsList = []
    all_rooms = db.child('buildings').child(str(building)).child(str(size)).get()
    #print(all_rooms)
    for room in all_rooms.each():
      if room.val() == "":
        roomsList.append(room.key())
  except:
    print("An error occurred: invalid arguments")
  return roomsList

def assignThis(blockID):
  """Assigns a single block to a room.

  Only to be used internally, this function determines the desired size of the
  room based on the number of people in a block, finds the first available room
  (searches through the block leader's desired buildings, in order) with the
  function findAvailableRooms, and calls the function assignment to complete 
  the assignment process for this block.


  Args:
    blockID: the unique ID for the block which is to be assigned to this room.
      This ID is defined by the userID of whoever creates the block.
  
    Returns:
      True if the process completed successfully. 
    Raises:
  
  """
  sizes = ["Singles", "Doubles", "Triples", "Quads"]
  #print(building)
  size = len(db.child('blocks').child(str(blockID)).child("Students in Block").get().each())
  size = sizes[size - 1]
  try:
    for i in range (0, 3):
      #print(i)
      building = db.child('users').child(str(blockID)).child('buildingPreference').get().each()[i].val() #TODO: this is finding it through the block leader's preference
      #print(building)
      availRooms = findAvailableRooms(building, size)
      if len(availRooms) == 0: #was >
        break
      assignment(blockID, building, size, availRooms[0])
      return True
  except:
    print("An error occurred: invalid arguments")
    return False

def assignAll():
  """Assigns all blocks to a rooms.

  Only to be used internally, iterates through all the blocks in db and calls
  assignThis with their blockID to place them into rooms.


  Args:
  
  Returns:
    True if this completed successfully
  Raises:
  
  """
  try:
    all_blocks = db.child('blocks').get()
    for block in all_blocks.each():
      assignThis(block.key())
    return True
  except:
    print("An error occurred: invalid arguments")
    return False

def clearAllRooms():
  """Removes all assignments for all rooms.

  Only to be used internally, iterates through every room for every size for
  every building in the database and sets the value of the rooms to "" if they
  had some value other than "" previously. This essentially keeps the room
  values around (doesn't fully delete a room) but removes people from them.


  Args:
  
  Returns:
    True if this completed successfully
  Raises:
  
  """
  try:
    all_buildings = db.child('buildings').get()
    for building in all_buildings.each():

      all_sizes = db.child('buildings').child(str(building.key())).get()
      for size in all_sizes.each():

        all_rooms = db.child('buildings').child(str(building.key())).child(str(size.key())).get()
        for room in all_rooms.each():

          if room.val() != "":
            db.child('buildings').child(str(building.key())).child(str(size.key())).update({room.key(): ""})
    return True
  except:
    print("An error occurred: clearAllRooms()")
    return False
  
def printAllRooms():
  """Prints info regarding which students occupy which rooms.

  This is an output function that prints the building name, then each room in
  the building along with the names of the students in those rooms. This text
  is sent to results.txt, and the names of the students are translated from IDs
  to literal names via uidToName().

  Args:
  
  Returns:
    A String with the exact same text as the updated results.txt.
  Raises:
  
  """
  fullOutput = ''
  try:
    all_buildings = db.child('buildings').get()
    for building in all_buildings.each():

      fullOutput += str(building.key()) + ":\n"
      all_sizes = db.child('buildings').child(str(building.key())).get()
      for size in all_sizes.each():

        all_rooms = db.child('buildings').child(str(building.key())).child(str(size.key())).get()
        for room in all_rooms.each():

          fullOutput += str("\tRoom ") + str(room.key()) + ":\n"
          if room.val() != "":
            all_people = db.child('buildings').child(str(building.key())).child(str(size.key())).child(str(room.key())).get()
            for person in all_people.each():


              fullOutput += "\t\t" + uidToName(str(person.val())) + "\n"
    outFile = open("results.txt", "w")
    outFile.write(fullOutput)
    outFile.close()
    return fullOutput
  except:
    return False

def uidToName(userID):
  """Converts userIDs to literal names.

  Given an input of a userID, this function parses through the 'users' section
  of the firebase and finds the name associated with that userID.

  Args:
    String userID to be converted to string
  Returns:
    The name of the student found via userID.
  Raises:
  
  """
  all_users = db.child('users').get()
  for user in all_users.each():
    if user.key() == userID:
      return db.child('users').child(str(user.key())).child('name').get().val()
  