window.SPRINTDASH = {
  state: null,
  map: null,
  liveWatchId: null,
};

async function apiFetch(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  return await res.json();
}

function toast(message, kind = "info") {
  const wrap = document.getElementById("toastWrap");
  if (!wrap) return;
  const el = document.createElement("div");
  el.className = "toast-item";
  el.innerHTML = `<strong>${kind.toUpperCase()}</strong><div>${message}</div>`;
  wrap.appendChild(el);
  setTimeout(() => el.remove(), 3000);
}

function updateRing(percent) {
  const ring = document.getElementById("progressRing");
  if (!ring) return;
  const deg = Math.max(0, Math.min(360, percent * 3.6));
  ring.style.setProperty("--progress", deg + "deg");
}

function setStatus(text) {
  const el = document.getElementById("statusText");
  if (el) el.textContent = text;
  const gps = document.getElementById("gpsStatus");
  if (gps) {
    if (text === "RUNNING") gps.textContent = "Running";
    else if (text === "FINISHED") gps.textContent = "Finished";
    else if (text === "ARMED") gps.textContent = "Armed";
    else gps.textContent = "GPS Ready";
  }
}

function formatTime(seconds) {
  seconds = Math.max(0, Number(seconds || 0));
  const minutes = Math.floor(seconds / 60);
  const secs = (seconds % 60).toFixed(2).padStart(5, "0");
  return `${String(minutes).padStart(2, "0")}:${secs}`;
}

function renderHistory(items) {
  const body = document.getElementById("historyBody");
  if (!body) return;
  body.innerHTML = "";
  items.forEach((item, idx) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${idx + 1}</td>
      <td>${item.date}</td>
      <td>${item.target_m}</td>
      <td>${item.distance_m}</td>
      <td>${item.time}</td>
      <td>${item.top_speed}</td>
      <td><span class="status-badge">${item.status}</span></td>
    `;
    body.appendChild(tr);
  });
}

async function refreshState() {
  try {
    const data = await apiFetch("/api/state");
    if (!data.ok) return;
    SPRINTDASH.state = data.state;
    syncUI(data.state);
  } catch (err) {
    console.error(err);
  }
}

function syncUI(state) {
  const target = Number(state.target_m || 0);
  const distance = Number(state.distance_m || 0);
  const remaining = Math.max(0, target - distance);
  const percent = target > 0 ? (distance / target) * 100 : 0;

  const set = (id, value) => {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
  };

  set("targetLabel", `${target} m`);
  set("progressTarget", `${target} m`);
  set("ringDistance", distance.toFixed(1));
  set("ringPercent", `${Math.min(999, percent).toFixed(2)}%`);
  set("remainingText", `Sisa ${remaining.toFixed(1)} m`);
  set("distanceM", distance.toFixed(1));
  set("distanceFt", Number(state.distance_ft || 0).toFixed(2));
  set("elapsedTime", formatTime(state.elapsed_time));
  set("currentSpeed", `${Number(state.current_speed || 0).toFixed(2)} m/s`);
  set("topSpeed", `${Number(state.top_speed || 0).toFixed(2)} m/s`);
  setStatus(state.status || "IDLE");
  set("gpsAccuracy", state.gps_accuracy ? `${Number(state.gps_accuracy).toFixed(1)} m` : "—");
  set("latLon", (state.lat !== null && state.lon !== null) ? `${Number(state.lat).toFixed(6)}, ${Number(state.lon).toFixed(6)}` : "—");
  updateRing(percent);

  if (SPRINTDASH.map && state.path && state.path.length && window.updateTrack) {
    window.updateTrack(state.path, state.lat, state.lon);
  }
}

async function refreshHistory() {
  try {
    const data = await apiFetch("/api/history");
    if (!data.ok) return;
    renderHistory(data.items || []);
  } catch (err) {
    console.error(err);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const themeToggle = document.getElementById("themeToggle");
  const root = document.documentElement;
  const savedTheme = localStorage.getItem("sprintdash-theme") || "dark";
  root.setAttribute("data-theme", savedTheme);
  if (themeToggle) {
    themeToggle.innerHTML = savedTheme === "dark" ? '<i class="bi bi-moon-stars"></i>' : '<i class="bi bi-sun-fill"></i>';
    themeToggle.addEventListener("click", () => {
      const newTheme = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", newTheme);
      localStorage.setItem("sprintdash-theme", newTheme);
      themeToggle.innerHTML = newTheme === "dark" ? '<i class="bi bi-moon-stars"></i>' : '<i class="bi bi-sun-fill"></i>';
    });
  }

  await refreshState();
  await refreshHistory();
  if (window.initMap) window.initMap();

  setInterval(refreshState, 1000);
  setInterval(refreshHistory, 5000);
});
