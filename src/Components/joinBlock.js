//function file -- handles logic for db stuff 

import { db } from '../firebaseConfig.js'; // Import your Firebase database reference
import { set, getDatabase, ref, child, get } from "firebase/database";

const joinBlock = async (userHofstraID, leaderHofstraID) => {
  try {
    // Check if the user is already in a block
    var userID = (await get(ref(db, 'localIdStorage/' + userHofstraID.toString()))).val();

    var inBlock = (await get(ref(db, 'users/' + userID + '/inBlock'))).val();

    if (inBlock !== '') {
      throw new Error('User is already in a block.');
    }

    // Check if the block under leaderID exists
    var leaderID = (await get(ref(db, 'localIdStorage/' + leaderHofstraID.toString()))).val();

    if (!leaderID) {
      throw new Error('Block under this leaderID does not exist.');
    }

    // Add the user to the block's student list
    //const blockList = leaderSnapshot.child('Students in Block').val() || [];
    var blockList = (await get(ref(db, 'blocks/' + leaderID + '/Students in Block'))).val();

    console.log(blockList);

    blockList.push(userID);
    await set(ref(db, 'blocks/' + leaderID + '/Students in Block'), blockList);

    // Update user's info to indicate the block they are in
    
    await set(ref(db, 'users/' + userID + '/inBlock'), leaderID);

    console.log('Successfully joined the block!');
  } catch (error) {
    console.error(error.message);
  }
};

export default joinBlock;
