import { getDatabase, ref, get, child } from 'firebase/database';
import { db } from '../firebaseConfig.js'; // Import your Firebase database reference
import { useState } from 'react';

  export const getTopUserList = async (userHofstraID) => {
      try {
        /*
          const dbRef = ref(getDatabase());
          const snapshot = await get(child(dbRef, preferenceLists/${userHofstraID}/topUserList));
          if (snapshot.exists()) {
              return snapshot.val();
          } else {
              console.error('No such document!');
          }*/
          var userList = (await get(ref(db, 'preferenceLists/' + userHofstraID.toString() + '/topUserList'))).val();
          return userList;

      } catch (error) {
          console.error('Error getting top user list:', error);
      }
  };

  export const getUserInfo = async (localIds) => {
      try {
          const users = [];
          for (const localId of localIds) {
            userName = (await get(ref(db, 'users/' + localId + '/name'))).val();
            email = (await get(ref(db, 'user/' + localId + '/userData/email'))).val();
            users.push( {
              'name' : userName,
              'email' : email
            }
          );

            /*
              const userRef = ref(getDatabase(), users/${localId});
              const snapshot = await get(userRef);
              if (snapshot.exists()) {
                  users.push({
                      name: snapshot.val().name,
                      userId: snapshot.key,
                  });
              }*/
          }
          return users;
      } catch (error) {
          console.error('Error getting user info:', error);
      }
  };