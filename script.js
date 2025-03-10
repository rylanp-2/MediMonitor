/* BEGIN Debug toggling */
const debugToggle = document.getElementById("debug-toggle");
const debugSection = document.querySelector(".debug");

function showDebug() {
  if (debugToggle.checked) {
    debugSection.classList.add("active");
  } else {
    debugSection.classList.remove("active");
  }
}

// Applies changes
debugToggle.addEventListener("change", showDebug);
window.addEventListener("load", showDebug);

/* END */
