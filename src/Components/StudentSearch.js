/*/ Function to send the fetch request
function createPreferenceLists() {
    fetch('/runPreferenceLists', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add any other headers if needed
      },
      // Add body data if needed
    })
    .then(response => {
      if (response.ok) {
        // Preference lists created successfully
        console.log('Preference lists created successfully');
      } else {
        // Handle error response
        console.error('Failed to create preference lists');
      }
    })
    .catch(error => {
      console.error('Error creating preference lists:', error);
    });
  }
  
  // Get the button element
  const button = document.getElementById('your-button-id');
  
  // Add a click event listener to the button
  button.addEventListener('click', () => {
    // Call the function to send the fetch request
    createPreferenceLists();
  });
  
  */