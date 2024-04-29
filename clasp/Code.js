// Define Firebase configuration
const firebaseConfig = {
    apiKey: "<REDACTED>",
    authDomain: "dorm-deciders.firebaseapp.com",
    databaseURL: "https://dorm-deciders-default-rtdb.firebaseio.com",
    projectId: "dorm-deciders",
    storageBucket: "dorm-deciders.appspot.com",
    messagingSenderId: "<REDACTED>",
    appId: "<REDACTED>",
    measurementId: "G-V8BYWBGHE6",
};

function processData(e) {
    var sheetId = "<REDACTED>";
    var sheet = SpreadsheetApp.openById(sheetId);
    var data = sheet.getDataRange().getValues();

    // Prepare data for Firebase
    var firebaseData = {};
    for (var i = 1; i < data.length; i++) {
        var item = data[i];
        var userID = item[4];
        firebaseData[userID] = {
            timeSubmitted: item[0],
            user: {
                name: item[1] + " " + item[2],
                dateOfBirth: item[3],
                userID: item[4],
                sex: item[5],
                accommodationInfo: item[6],
                classStanding: item[7] === "First Year" ? "Freshman"
                    : item[7],
            },
            housing: {
                roomType:
                    item[10] !== ""
                        ? item[10]
                        : item[11] !== ""
                          ? item[11]
                          : item[12] !== ""
                            ? item[12]
                            : "Quad Room",
                firstChoice:
                    item[13] !== ""
                        ? item[13]
                        : item[16] !== ""
                          ? item[16]
                          : item[19] !== ""
                            ? item[19]
                            : "Graduate Residence Hall",
                secondChoice:
                    item[14] !== ""
                        ? item[14]
                        : item[17] !== ""
                          ? item[17]
                          : item[20] !== ""
                            ? item[20]
                            : undefined,
                thirdChoice:
                    item[15] !== ""
                        ? item[15]
                        : item[18] !== ""
                          ? item[18]
                          : item[21] !== ""
                            ? item[21]
                            : undefined,
            },
            preferences: {
                floorEnvironment: item[22],
                floorLevel: item[23],
                studyHabits: item[24],
                cleanliness: item[25],
                willResideWithTransRoommate:
                    item[26] ===
                    "I am not comfortable residing with a transgender or non-conforming roommate or suitemate"
                        ? false
                        : true,
                bedtime: item[27],
                roommateSex: item[28]
            },
        };
    }
    // Write data to Firebase Realtime Database
    var firebaseUrl = firebaseConfig.databaseURL + "/studentQuestionnaireResponses.json";
    var options = {
        method: "put",
        contentType: "application/json",
        payload: JSON.stringify(firebaseData),
    };
    var response = UrlFetchApp.fetch(firebaseUrl + "?auth=" + firebaseConfig.apiKey, options);

    // Log response from Firebase
    Logger.log(response.getContentText());

    return ContentService.createTextOutput("Data imported successfully");
}
