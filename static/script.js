/* BEGIN Debug info */
const debugToggle = document.getElementById("debug-toggle");
const debugSection = document.querySelector(".debug");

/**
 * dynamically shows debug section depending on tickbox
 */
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

// Updates debug section with provided values
function debugValues(t1, t2, t3, at, ut) {
  document.getElementById("t1").textContent = "Temperature 1: " + t1;
  document.getElementById("t2").textContent = "Temperature 2: " + t2;
  document.getElementById("t3").textContent = "Temperature 3: " + t3;
  document.getElementById("at").textContent = "Average: " + at;
  document.getElementById("ut").textContent = "Unix Time: " + ut;
  // Hides status message
  document.getElementById("not-connected").style.display = "none";
}

/* END */

/* BEGIN Stop server button */

document.getElementById("stop-server").addEventListener("click", function () {
  if (
    confirm(
      "Are you sure you want to stop the server? It will need to be restarted manually.",
    )
  ) {
    console.log("Stopping Server");
    document.getElementById("not-connected").style.display = "inherit";
    fetch("/shutdown", { method: "GET" }); // sends shutdown command to websocket server
  }
});

/* END */

/* BEGIN input handling */

const inputTempHigh = document.getElementById("temp-input-high");
const inputTempLow = document.getElementById("temp-input-low");

/**
 * grabs user inputted values for config
 * @returns {Array} low, high value in an array
 */
function getTempConfig() {
  let high = document.querySelector("#temp-input-high").valueAsNumber;
  let low = document.querySelector("#temp-input-low").valueAsNumber;
  return { low, high };
}

/**
 * ensures the user inputs a valid temperature range before submission
 */
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

/* END */

/* BEGIN Websocket shenanigans */

/* BEGIN premade code - author: donsky@donskytech.com */
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

/* END premade code */

/**
 * handles incoming websocket messages from the Pi
 * @param {string} csv event message recieved by microdot
 */
function onMessage(event) {
  let values = event.data.split(", ");
  // Figure out type of info sent
  let type = values[0].trim();

  if (type == "config") {
    console.log("Config received:", event);
    let tempConfigUpper = values[1].trim();
    let tempConfigLower = values[2].trim();

    inputTempHigh.value = tempConfigUpper;
    inputTempLow.value = tempConfigLower;
  }

  if (type == "data") {
    // console.log("Temperatures received:", event);
    // Individual Temperatures
    let temp1 = values[1].trim();
    let temp2 = values[2].trim();
    let temp3 = values[3].trim();
    let avgTemp = parseFloat(values[4]) || 0; // Turns into float
    let humidity = values[5].trim();
    let unixTime = values[6].trim();
    let tempStatus = values[7].trim();

    // Updates main status
    updateStatus(tempStatus, 1, avgTemp, humidity); // 1 is a placeholder for humidity status

    // Throws remaining values into debug section
    debugValues(temp1, temp2, temp3, avgTemp, unixTime);

    // console.log("Pi Time:", unixTime);
  }

  submitButton.setCustomValidity("");
  updateSubmitButton();
}

/* BEGIN data sending */

function sendMessage(message) {
  websocket.send(message);
}

const configForm = document.querySelector(".form-area");
const submitButton = document.getElementById("button");

/**
 * updates the submit button
 */
function updateSubmitButton() {
  submitButton.checkValidity();
  submitButton.reportValidity();
}

/**
 * sumbits validated temperature range configuration to the Pi
 */
configForm.addEventListener("submit", function (event) {
  event.preventDefault();

  let temp = getTempConfig();

  if (websocket.readyState === WebSocket.OPEN) {
    let data = temp.high + ", " + temp.low;
    sendMessage(data);
    console.log("Sent to WebSocket:", data);
  } else {
    console.error("WebSocket is not open!");
    submitButton.setCustomValidity("WebSocket is not open!");
    updateSubmitButton();
  }
});
/* END */

/* END */

/* BEGIN status updating */

const statusTemperature = document.getElementById("status-temperature");
const statusHumidity = document.getElementById("status-humidity");
const statTempIcon = document.getElementById("stat-temp-icon");
const statHumIcon = document.getElementById("stat-hum-icon");
var statTemp = 1;
var statHum = 1;

/**
 * updates the main status display
 * @param {number} tempStatus temperature status from the Pi
 * @param {number} humStatus humidity status from the Pi
 * @param {number} avgTemp temperature to display
 * @param {number} humidity humidity to display
 */
function updateStatus(tempStatus, humStatus, avgTemp, humidity) {
  document.documentElement.style.setProperty("--status-content", `""`);
  statusTemperature.textContent = avgTemp.toFixed(1) + " °C"; // rounds value to one place
  statusHumidity.textContent = humidity + "%";

  statTemp = checkIconStatus(statTempIcon, tempStatus, statTemp);
  statHum = checkIconStatus(statHumIcon, humStatus, statHum);
}

/**
 * updates the icon graphic depending on passed value
 * @param {Element} iconType some icon with class "status"
 * @param {number} status status from hardware
 * @param {number} storedStatus status stored in memory
 * @returns status passed to the function, unchanged
 */
function checkIconStatus(iconType, status, storedStatus) {
  if (status != storedStatus) {
    iconType.classList.remove("stat-good", "stat-bad", "stat-warn");
    if (status == 0) {
      iconType.classlist.add("stat-good");
    } else if (status == 1) {
      iconType.classList.add("stat-warn");
    } else {
      iconType.classList.add("stat-bad");
    }
  }
  return status;
}
/* END */
