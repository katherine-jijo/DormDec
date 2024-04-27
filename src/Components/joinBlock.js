//function file -- handles logic for db stuff 

import { db } from '../firebaseConfig.js'; // Import your Firebase database reference

const joinBlock = async (userID, leaderID) => {
  try {
    // Check if the user is already in a block
    const userRef = db.ref(`users/${userID}`);
    const userSnapshot = await userRef.once('value');
    const inBlock = userSnapshot.child('inBlock').val();

    if (inBlock !== '') {
      throw new Error('User is already in a block.');
    }

    // Check if the block under leaderID exists
    const leaderRef = db.ref(`blocks/${leaderID}`);
    const leaderSnapshot = await leaderRef.once('value');
    if (!leaderSnapshot.exists()) {
      throw new Error('Block under this leaderID does not exist.');
    }

    // Add the user to the block's student list
    const blockList = leaderSnapshot.child('Students in Block').val() || [];
    blockList.push(userID);
    await leaderRef.update({
      'Students in Block': blockList,
    });

    // Update user's info to indicate the block they are in
    await userRef.update({
      inBlock: leaderID,
    });

    console.log('Successfully joined the block!');
  } catch (error) {
    console.error(error.message);
  }
};

export default joinBlock;
