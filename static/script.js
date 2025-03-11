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

/* BEGIN Websocket shenanigans */

const statusTemperature = document.querySelector("status-temperature");
const statusHumidity = document.querySelector("status-humidity");

var targetUrl = `ws://${location.host}/ws`;
var websocket;
window.addEventListener("load", onLoad);

function onLoad() {
  initializeSocket();
}

function initializeSocket() {
  console.log("Opening WebSocket connection MicroPython Server...");
  websocket = new WebSocket(targetUrl);
  websocket.onopen = onOpen;
  websocket.onclose = onClose;
  websocket.onmessage = onMessage;
}
function onOpen(event) {
  console.log("Starting connection to WebSocket server..");
}
function onClose(event) {
  console.log("Closing connection to server..");
  setTimeout(initializeSocket, 2000);
}
function onMessage(event) {
  console.log("WebSocket message received:", event);
  updateValues(event.data);
  updateChart(event.data);
}

function sendMessage(message) {
  websocket.send(message);
}
