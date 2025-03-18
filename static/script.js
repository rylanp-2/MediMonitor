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

/* BEGIN Stop server button */
var stopServer = false;

document.getElementById("stop-server").addEventListener("click", function () {
  if (
    confirm(
      "Are you sure you want to stop the server? It will need to be restarted manually.",
    )
  ) {
    // TODO: placeholder
    console.log("Stopping Server");
    stopServer = true;
  }
});

/* END */

/* BEGIN input handling */

const inputTempHigh = document.getElementById("temp-input-high");
const inputTempLow = document.getElementById("temp-input-low");

// Reusable function for grabbing config values set by user
function getTempConfig() {
  let high = document.querySelector("#temp-input-high").valueAsNumber;
  let low = document.querySelector("#temp-input-low").valueAsNumber;
  return { low, high };
}

// Ensures the user inputs a valid temperature range before submission
function tempRange() {
  const temp = getTempConfig();

  if (temp.low > temp.high) {
    inputTempHigh.setCustomValidity(
      "Number must be above the lower temperature",
    );
    inputTempLow.setCustomValidity(
      "Number must be below the higher temperature",
    );
  } else {
    inputTempHigh.setCustomValidity("");
    inputTempLow.setCustomValidity("");
  }
  inputTempHigh.checkValidity();
  inputTempLow.checkValidity();

  // Ensure only the currently focused field displays validation errors
  if (document.activeElement === inputTempHigh) {
    inputTempHigh.reportValidity();
  } else if (document.activeElement === inputTempLow) {
    inputTempLow.reportValidity();
  }
}

// Watches for changes
tempRange();

inputTempHigh.addEventListener("input", tempRange);
inputTempLow.addEventListener("input", tempRange);

// Capture config, send to the pi
const configForm = document.querySelector(".form-area");

configForm.addEventListener("submit", function (event) {
  event.preventDefault();

  temp = getTempConfig();

  // TODO: placeholder for sending to pi
  console.log("High:", temp.high);
  console.log("Low:", temp.low);
});

/* END */

/* BEGIN Websocket shenanigans */

const statusTemperature = document.querySelector("status-temperature");
const statusHumidity = document.querySelector("status-humidity");

var targetUrl = `ws://${location.host}/ws`;
var websocket;
window.addEventListener("load", onLoad);

function onLoad() {
  if ((stopServer = false)) {
    initializeSocket();
  }
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
  // updateValues(event.data);
  // updateChart(event.data);
  consile.log("Values:", event.data);
}

function sendMessage(message) {
  websocket.send(message);
}
querySelector;
