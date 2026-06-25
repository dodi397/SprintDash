function initMap() {
  const el = document.getElementById("map");
  if (!el || typeof L === "undefined") return;

  const defaultCenter = [-6.208763, 106.845599];
  const map = L.map("map", { zoomControl: true }).setView(defaultCenter, 15);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  const startIcon = L.divIcon({
    className: "track-marker start-marker",
    html: '<div style="width:18px;height:18px;border-radius:50%;background:#33ff77;box-shadow:0 0 16px #33ff77;border:3px solid #fff"></div>',
    iconSize: [18, 18],
    iconAnchor: [9, 9],
  });

  const endIcon = L.divIcon({
    className: "track-marker end-marker",
    html: '<div style="width:18px;height:18px;border-radius:50%;background:#ff4747;box-shadow:0 0 16px #ff4747;border:3px solid #fff"></div>',
    iconSize: [18, 18],
    iconAnchor: [9, 9],
  });

  let polyline = L.polyline([], { color: "#57ff66", weight: 5, opacity: 0.9 }).addTo(map);
  let startMarker = L.marker(defaultCenter, { icon: startIcon }).addTo(map);
  let endMarker = L.marker(defaultCenter, { icon: endIcon }).addTo(map);

  window.updateTrack = function(path, lat, lon) {
    if (!path || !path.length) return;
    const points = path.map(p => [p.lat, p.lon]);
    polyline.setLatLngs(points);
    const first = points[0];
    const last = points[points.length - 1];
    startMarker.setLatLng(first);
    endMarker.setLatLng(last);
    map.panTo(last, { animate: true });
  };

  window.resetMapTrack = function() {
    polyline.setLatLngs([]);
    startMarker.setLatLng(defaultCenter);
    endMarker.setLatLng(defaultCenter);
    map.setView(defaultCenter, 15);
  };

  window.setMapCenter = function(lat, lon) {
    map.setView([lat, lon], 17);
    startMarker.setLatLng([lat, lon]);
    endMarker.setLatLng([lat, lon]);
  };

  SPRINTDASH.map = map;
}
window.initMap = initMap;
