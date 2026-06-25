async function requestLocationPermission() {
  if (!navigator.geolocation) {
    toast("Browser tidak mendukung geolocation.", "error");
    return;
  }

  navigator.geolocation.getCurrentPosition(async (pos) => {
    const payload = {
      lat: pos.coords.latitude,
      lon: pos.coords.longitude,
      accuracy: pos.coords.accuracy,
    };
    try {
      const res = await apiFetch("/race/location", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        toast("Lokasi berhasil diambil.", "success");
        SPRINTDASH.state = res.state;
        syncUI(res.state);
        if (window.setMapCenter) window.setMapCenter(payload.lat, payload.lon);
      } else {
        toast(res.message || "Gagal mengambil lokasi.", "error");
      }
    } catch (e) {
      toast("Error saat mengambil lokasi.", "error");
    }
  }, (err) => {
    toast(err.message || "Izin lokasi ditolak.", "error");
  }, {
    enableHighAccuracy: true,
    timeout: 10000,
    maximumAge: 0,
  });
}

async function startLiveWatch() {
  if (!navigator.geolocation) return;
  if (SPRINTDASH.liveWatchId) navigator.geolocation.clearWatch(SPRINTDASH.liveWatchId);

  SPRINTDASH.liveWatchId = navigator.geolocation.watchPosition(async (pos) => {
    const payload = {
      lat: pos.coords.latitude,
      lon: pos.coords.longitude,
      accuracy: pos.coords.accuracy,
    };
    try {
      const res = await apiFetch("/race/update", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      if (res.ok) {
        SPRINTDASH.state = res.state;
        syncUI(res.state);
      }
    } catch (e) {
      console.error(e);
    }
  }, (err) => {
    console.warn(err);
  }, {
    enableHighAccuracy: true,
    maximumAge: 0,
    timeout: 10000,
  });
}
