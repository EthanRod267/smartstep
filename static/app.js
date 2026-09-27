const API_BASE = "http://127.0.0.1:5000"; // change to your deployed backend URL later

const connectBtn = document.getElementById("connectBtn");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const readingsBody = document.getElementById("readingsBody");
const suggestionsList = document.getElementById("suggestionsList");

const formRatingVal = document.getElementById("formRatingVal");
const speedVal = document.getElementById("speedVal");

// ---- 1. Web Bluetooth connection ----
// NOTE: Replace SERVICE_UUID / CHARACTERISTIC_UUID with the actual UUIDs
// your shoe's firmware advertises. These are placeholders.
const SERVICE_UUID = "0000xxxx-0000-1000-8000-00805f9b34fb";
const CHARACTERISTIC_UUID = "0000yyyy-0000-1000-8000-00805f9b34fb";

connectBtn.addEventListener("click", async () => {
  try {
    statusText.textContent = "Requesting device...";

    const device = await navigator.bluetooth.requestDevice({
      filters: [{ services: [SERVICE_UUID] }]
    });

    statusText.textContent = `Connecting to ${device.name}...`;
    const server = await device.gatt.connect();
    const service = await server.getPrimaryService(SERVICE_UUID);
    const characteristic = await service.getCharacteristic(CHARACTERISTIC_UUID);

    await characteristic.startNotifications();
    characteristic.addEventListener("characteristicvaluechanged", handleSensorData);

    statusDot.classList.add("connected");
    statusText.textContent = `Connected — ${device.name}`;
  } catch (err) {
    console.error(err);
    statusDot.classList.remove("connected");
    statusText.textContent = `Error: ${err.message}`;
  }
});

// ---- 2. Parse incoming BLE data and send the RAW reading to the backend ----
// Note: form_rating, speed, and suggestions are computed server-side
// (in analysis.py) — the frontend only ever sends raw sensor values.
function handleSensorData(event) {
  const value = event.target.value; // DataView

  // TODO: Replace this parsing logic with whatever byte layout your
  // firmware actually sends.
  const reading = {
    device_id: "shoe_left_01",
    pressure: value.getFloat32(0, true),
    gyro: {
      x: value.getFloat32(4, true),
      y: value.getFloat32(8, true),
      z: value.getFloat32(12, true)
    },
    frequency: value.getFloat32(16, true)
  };

  sendReading(reading);
}

// ---- 3. Send a raw reading to the Flask API (server computes the metrics) ----
async function sendReading(reading) {
  try {
    await fetch(`${API_BASE}/readings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(reading)
    });
    // Pull the latest computed data back down after the insert
    loadReadings();
  } catch (err) {
    console.error("Failed to send reading:", err);
  }
}

// ---- 4. Fetch and display recent computed readings from MongoDB ----
async function loadReadings() {
  try {
    const res = await fetch(`${API_BASE}/readings?limit=20`);
    const readings = await res.json();

    readingsBody.innerHTML = "";
    chart.data.labels = [];
    chart.data.datasets[0].data = [];

    // oldest first on the chart / table
    readings.slice().reverse().forEach((r) => {
      addRowToTable(r);
      pushChartPoint(r);
    });

    if (readings.length > 0) {
      updateReadouts(readings[0]);
      updateSuggestions(readings[0].suggestions);
    }
  } catch (err) {
    console.error("Failed to load readings:", err);
  }
}

// ---- 5. UI helpers ----
function updateReadouts(r) {
  formRatingVal.textContent = r.form_rating ?? "--";
  speedVal.textContent = r.speed ?? "--";
}

function updateSuggestions(suggestions) {
  suggestionsList.innerHTML = "";
  (suggestions || []).forEach((s) => {
    const li = document.createElement("li");
    li.textContent = s;
    suggestionsList.appendChild(li);
  });
}

function addRowToTable(r) {
  const row = document.createElement("tr");
  const time = r.timestamp ? r.timestamp.split("T")[1]?.split(".")[0] : "-";
  row.innerHTML = `
    <td>${time ?? "-"}</td>
    <td>${r.device_id ?? "-"}</td>
    <td>${r.form_rating ?? "-"}</td>
    <td>${r.speed ?? "-"}</td>
  `;
  readingsBody.prepend(row);
}

// ---- 6. Chart.js live speed chart ----
const ctx = document.getElementById("speedChart").getContext("2d");
const chart = new Chart(ctx, {
  type: "line",
  data: {
    labels: [],
    datasets: [{
      label: "Speed (m/s)",
      data: [],
      borderColor: "#4c8bf5",
      backgroundColor: "rgba(76, 139, 245, 0.1)",
      tension: 0.3,
      fill: true,
      pointRadius: 0
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: {
      x: { ticks: { color: "#8a93a1" }, grid: { color: "#2a2f38" } },
      y: { ticks: { color: "#8a93a1" }, grid: { color: "#2a2f38" } }
    }
  }
});

function pushChartPoint(r) {
  const time = r.timestamp ? r.timestamp.split("T")[1]?.split(".")[0] : "";
  chart.data.labels.push(time);
  chart.data.datasets[0].data.push(r.speed);
  if (chart.data.labels.length > 20) {
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
  }
  chart.update();
}

// Load existing readings on page load, then refresh periodically
loadReadings();
setInterval(loadReadings, 5000);
