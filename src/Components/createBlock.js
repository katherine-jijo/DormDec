// createBlock.js
//function file -- handles logic for db stuff 


import { db } from '../firebaseConfig.js'; // Import your Firebase database reference

const createBlock = async (userID) => {
  try {
    // Check if the user is already in a block
    const userRef = db.ref(`users/${userID}`);
    const userSnapshot = await userRef.once('value');
    const inBlock = userSnapshot.child('inBlock').val();

    if (inBlock !== '') {
      throw new Error('User is already in a block.');
    }

    // Get user's information
    const userInfoSnapshot = await userRef.once('value');
    const userName = userInfoSnapshot.child('name').val();
    const buildingPreference = userInfoSnapshot.child('buildingPreference').val()[0];

    // Create block data
    const blockData = {
      'Block Leader': userName,
      'Students in Block': [userID],
      'Building': buildingPreference,
    };

    // Create the block under the creator's userID
    await db.ref('blocks').child(userID).set(blockData);

    // Update user's info to indicate the block they are in
    await userRef.update({
      inBlock: userID,
    });

    console.log('Block created successfully!');
  } catch (error) {
    console.error(error.message);
  }
};

export default createBlock;
