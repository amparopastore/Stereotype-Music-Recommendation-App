// Spotify Client ID
const CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID';
// Redirect URI after authorization
const REDIRECT_URI = 'http://localhost:8080/callback'; // Update with your actual redirect URI
// Trending Artists
const TRENDING_ARTISTS = ['Artist 1', 'Artist 2', 'Artist 3', 'Artist 4', 'Artist 5']; // Sample trending artists

document.addEventListener("DOMContentLoaded", function() {
    // Your Firebase configuration
    var firebaseConfig = {
        apiKey: "YOUR_API_KEY",
        authDomain: "YOUR_AUTH_DOMAIN",
        projectId: "YOUR_PROJECT_ID",
        storageBucket: "YOUR_STORAGE_BUCKET",
        messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
        appId: "YOUR_APP_ID"
    };
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);

    // Get references to HTML elements
    var searchInput = document.getElementById('searchInput');
    var searchBtn = document.getElementById('searchBtn');
    var searchResults = document.getElementById('searchResults');
    var logoutBtn = document.getElementById('logoutBtn');
    var linkSpotifyBtn = document.getElementById('linkSpotifyBtn');

    // Add event listener for search button click
    searchBtn.addEventListener('click', function() {
        var searchTerm = searchInput.value;
        // Implement logic to search for music using searchTerm
        // Display search results in searchResults div
        searchResults.innerHTML = "<p>Search results for: " + searchTerm + "</p>";
    });

    // Check if user is authenticated
    firebase.auth().onAuthStateChanged(function(user) {
        if (user) {
            // User is signed in
            console.log('User signed in:', user);
            logoutBtn.style.display = 'block'; // Show logout button
        } else {
            // User is signed out
            console.log('User signed out');
            logoutBtn.style.display = 'none'; // Hide logout button
        }
    });

    // Add event listener for logout button click
    logoutBtn.addEventListener('click', function() {
        firebase.auth().signOut().then(function() {
            console.log('User signed out');
        }).catch(function(error) {
            console.error('Sign out error:', error);
        });
    });

    // Function to open Spotify authorization popup
    function linkSpotify() {
        // Replace with the Spotify authorization URL
        var spotifyAuthUrl = 'https://accounts.spotify.com/authorize';
        var popupWindow = window.open(spotifyAuthUrl, '_blank', 'width=600,height=600');
        // Check if the popup window is closed
        var interval = setInterval(function() {
            if (popupWindow.closed) {
                clearInterval(interval);
                // Handle popup closed event
                console.log('Popup window closed');
            }
        }, 1000);
    }

    // Add event listener for link Spotify button click
    linkSpotifyBtn.addEventListener('click', linkSpotify);
});


// Function to display trending artists carousel
function displayTrendingArtists() {
  const carousel = document.getElementById('artistsCarousel');
  TRENDING_ARTISTS.forEach(artist => {
    const artistElement = document.createElement('div');
    artistElement.classList.add('artist');
    // Sample artist image (replace with actual images)
    artistElement.innerHTML = `
      <img src="artist_${artist.toLowerCase().replace(/\s/g, '_')}.jpg" alt="${artist}">
      <p>${artist}</p>
    `;
    carousel.appendChild(artistElement);
  });
}

// Assuming accessToken is obtained after user authorization

// Display trending artists
if (document.getElementById('artistsCarousel')) {
  displayTrendingArtists();
}
