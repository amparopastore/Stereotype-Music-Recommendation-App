// DROPDOWN MENU
document.addEventListener("DOMContentLoaded", function() {
    const customDropdownButton = document.getElementById("customDropdownButton");
    const customDropdownMenu = document.getElementById("customDropdownMenu");
  
    customDropdownButton.addEventListener("click", function() {
      if (customDropdownMenu.style.display === "block") {
        customDropdownMenu.style.display = "none";
      } else {
        customDropdownMenu.style.display = "block";
      }
    });
  
    document.addEventListener("click", function(event) {
      if (!customDropdownButton.contains(event.target) && !customDropdownMenu.contains(event.target)) {
        customDropdownMenu.style.display = "none";
      }
    });
  });


// ANIMATION FOR DASHBOARD PHOTOS
document.addEventListener("DOMContentLoaded", function() {
    const horizontalScrolls = document.querySelectorAll(".horizontal-scroll");

    horizontalScrolls.forEach(function(horizontalScroll) {
        horizontalScroll.addEventListener("mouseover", function() {
            pauseAnimation(horizontalScroll);
        });

        horizontalScroll.addEventListener("mouseout", function() {
            resumeAnimation(horizontalScroll);
        });
    });
});

function pauseAnimation(element) {
    const scrollItems = element.querySelectorAll("ul.artists-list, ul.tracks-list");
    scrollItems.forEach(function(item) {
        item.style.animationPlayState = "paused";
    });
}

function resumeAnimation(element) {
    const scrollItems = element.querySelectorAll("ul.artists-list, ul.tracks-list");
    scrollItems.forEach(function(item) {
        item.style.animationPlayState = "running";
    });
}

  