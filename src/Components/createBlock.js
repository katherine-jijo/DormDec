// createBlock.js
//function file -- handles logic for db stuff 


import { db } from '../firebaseConfig.js'; // Import your Firebase database reference
import { ref, get, set } from "firebase/database"

const createBlock = async (userHofstraID) => {
  try {
    //const dbRef = ref(getDatabase());
    var userID = (await get(ref(db, 'localIdStorage/' + userHofstraID.toString()))).val();

    //console.log(userID)
    
    var inBlock = (await get(ref(db, 'users/' + userID + '/inBlock'))).val();
    //console.log(inBlock);

    if (inBlock != '') {
      //console.log(inBlock)
      throw new Error('User is already in a block.');
    }

    // Get user's information
    var buildingPreference = (await get(ref(db, 'users/' + userID + '/buildingPreference'))).val()[0];
    var userName = (await get(ref(db, 'users/' + userID + '/name'))).val();
    //console.log(buildingPreference);
    //console.log(userName);

    // Create block data
    const blockData = {
      'Block Leader': userName,
      'Students in Block': [userID],
      'Building': buildingPreference,
    };
    //console.log(blockData)

    
    // Create the block under the creator's userID
    await set(ref(db, 'blocks/' + userID), blockData);

    await set(ref(db, 'users/' + userID + '/inBlock'), userID);

    console.log('Block created successfully!');
  } catch (error) {
    console.error(error.message);
  }
};

export default createBlock;
