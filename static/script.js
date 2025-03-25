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
    console.log("Stopping Server");
    stopServer = true;
    window.location.href =
      "/shutdown"; /* sends shutdown command to websocket server */
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

  let temp = getTempConfig();

  if (websocket.readyState === WebSocket.OPEN) {
    let data = JSON.stringify({ high: temp.high, low: temp.low });
    websocket.send(data);
    console.log("Sent to WebSocket:", data);
  } else {
    console.error("WebSocket is not open!");
  }
});

/* END */

/* BEGIN Websocket shenanigans */

const statusTemperature = document.querySelector("#status-temperature");
const statusHumidity = document.querySelector("#status-humidity");

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

  let values = event.data.split(", ");
  // Individual Temperatures
  // let temp1 = values[0].trim();
  // let temp2 = values[1].trim();
  // let temp3 = values[2].trim();
  let avgTemp = parseFloat(values[3]) || 0;
  let humidity = values[4].trim();
  let unixTime = values[5].trim();

  document.documentElement.style.setProperty("--status-content", `""`);
  statusTemperature.textContent = avgTemp.toFixed(1) + " °C";
  statusHumidity.textContent = humidity + "%";

  console.log("Pi Time:", unixTime);
  // console.log("Values:", event.data);
}

function sendMessage(message) {
  websocket.send(message);
}
querySelector;
