//function file -- handles logic for db stuff 


// Import your Firebase database reference

const leaveBlock = async (userID) => {
  try {
    // Get leaderID from user's inBlock field
    const userRef = db.ref(`users/${userID}`);
    const userSnapshot = await userRef.once('value');
    const leaderID = userSnapshot.child('inBlock').val();

    if (leaderID !== '') {
      // Retrieve blockList
      const blockListRef = db.ref(`blocks/${leaderID}/Students in Block`);
      const blockListSnapshot = await blockListRef.once('value');
      let blockList = blockListSnapshot.val() || [];

      // Remove user from blockList
      blockList = blockList.filter((student) => student !== userID);

      // Update block with updated blockList
      await blockListRef.set(blockList);

      // Update user's inBlock field to indicate they are no longer in a block
      await userRef.update({
        inBlock: '',
      });

      // Delete block if blockList is empty
      if (blockList.length === 0) {
        await db.ref(`blocks/${leaderID}`).remove();
      } else if (leaderID === userID) { // Check if the user is the leader
        // Choose the next leader
        const newLeader = blockList[0];

        // Update new leader's inBlock field
        await db.ref(`users/${newLeader}`).update({
          inBlock: '',
        });

        // Create a new block under the new leader's userID
        // Implement your createBlock logic here

        // Remove other students from old block and add them to the new block
        for (const student of blockList) {
          if (student === newLeader) continue;

          // Remove student from old block
          await db.ref(`users/${student}`).update({
            inBlock: '',
          });

          // Join student to new block
          // Implement your joinBlock logic here
        }

        // Delete the old block
        await db.ref(`blocks/${leaderID}`).remove();
      }

      console.log('Successfully left the block!');
    } else {
      throw new Error('User is not in a block.');
    }
  } catch (error) {
    console.error(error.message);
  }
};

export default leaveBlock;
