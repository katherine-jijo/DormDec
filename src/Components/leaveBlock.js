//function file -- handles logic for db stuff 
import { db } from '../firebaseConfig.js'; // Import your Firebase database reference
import { set, getDatabase, ref, child, get } from "firebase/database";

// Import your Firebase database reference

const leaveBlock = async (userHofstraID) => {
  try {
    var userID = (await get(ref(db, 'localIdStorage/' + userHofstraID.toString()))).val();

    // Get leaderID from user's inBlock field
    var leaderID = (await get(ref(db, 'users/' + userID + '/inBlock'))).val();

    if (leaderID != '') {
      // Retrieve blockList
      var blockList = (await get(ref(db, 'blocks/' + leaderID + '/Students in Block'))).val();
      
      /*
      const blockListRef = db.ref(`blocks/${leaderID}/Students in Block`);
      const blockListSnapshot = await blockListRef.once('value');
      let blockList = blockListSnapshot.val() || [];
      */

      // Remove user from blockList
      blockList = blockList.filter((student) => student != userID);

      // Update block with updated blockList
      //await blockListRef.set(blockList);
      await set(ref(db, 'blocks/' + leaderID + '/Students in Block'), blockList);

      // Update user's inBlock field to indicate they are no longer in a block
      await set(ref(db, 'users/' + userID + '/inBlock'), '');

      /*
      await userRef.update({
        inBlock: '',
      });
      */

      // Delete block if blockList is empty
      if (blockList.length == 0) {
        await set(ref(db, 'blocks/' + leaderID), null);

      } else if (leaderID == userID) { // Check if the user is the leader
        // Choose the next leader
        const newLeader = blockList[0];

        // Update new leader's inBlock field
        await set(ref(db, 'users/' + newLeader + '/inBlock'), '');

        // Create a new block under the new leader's userID
        // Implement your createBlock logic here
        //Create block logic
        var buildingPreference = (await get(ref(db, 'users/' + newLeader + '/buildingPreference'))).val()[0];
        var userName = (await get(ref(db, 'users/' + newLeader + '/name'))).val();
        const blockData = {
          'Block Leader': userName,
          'Students in Block': [newLeader],
          'Building': buildingPreference,
        };

        await set(ref(db, 'blocks/' + newLeader), blockData);

        await set(ref(db, 'users/' + newLeader + '/inBlock'), newLeader);

        console.log('Block created successfully!');

        // Remove other students from old block and add them to the new block
        for (const student of blockList) {
          if (student == newLeader) continue;

          // Remove student from old block
          await set(ref(db, 'users/' + student + '/inBlock'), '');

          // Join student to new block
          // Implement your joinBlock logic here
          blockList.push(student)
          await set(ref(db, 'users/' + student + '/inBlock'), newLeader);

        }
        await set(ref(db, 'blocks/' + leaderID + '/Students in Block'), blockList);

        // Delete the old block
        await set(ref(db, 'blocks/' + leaderID), null);
      }

      //console.log('Successfully left the block!');
      
    } else {
      throw new Error('User is not in a block.');
    }
  } catch (error) {
    console.error(error.message);
  }
};

export default leaveBlock;
