/* BEGIN Debug toggling */
const debugToggle = document.getElementById("debug-toggle");
const debugSection = document.querySelector(".debug");

function showDebug() {
  if (debugToggle.checked) {
    debugSection.style.opacity = "1";
    debugSection.style.height = "auto";
  } else {
    debugSection.style.opacity = "0";
    debugSection.style.height = "0";
  }
}

// Applies changes
debugToggle.addEventListener("change", showDebug);
window.addEventListener("load", showDebug);

/* END */
