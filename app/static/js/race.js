async function postRace(url, body = {}) {
  return await apiFetch(url, {
    method: "POST",
    body: JSON.stringify(body),
  });
}

document.addEventListener("DOMContentLoaded", () => {
  const targetInput = document.getElementById("targetInput");
  const btnLocation = document.getElementById("btnLocation");
  const btnStart = document.getElementById("btnStart");
  const btnStop = document.getElementById("btnStop");
  const btnReset = document.getElementById("btnReset");
  const clearHistoryBtn = document.getElementById("clearHistoryBtn");

  if (targetInput) {
    targetInput.addEventListener("change", async () => {
      const target_m = Number(targetInput.value || 0);
      const res = await postRace("/race/target", { target_m });
      if (res.ok) {
        syncUI(res.state);
      } else {
        toast(res.message || "Target tidak valid.", "error");
      }
    });
  }

  btnLocation?.addEventListener("click", requestLocationPermission);

  btnStart?.addEventListener("click", async () => {
    const res = await postRace("/race/start");
    if (res.ok) {
      toast("Race armed. Bergerak untuk mulai timer.", "success");
      syncUI(res.state);
      startLiveWatch();
    } else {
      toast(res.message || "Gagal start.", "error");
    }
  });

  btnStop?.addEventListener("click", async () => {
    const res = await postRace("/race/stop");
    if (res.ok) {
      toast("Race dihentikan.", "warning");
      syncUI(res.state);
    }
  });

  btnReset?.addEventListener("click", async () => {
    const res = await postRace("/race/reset");
    if (res.ok) {
      toast("Dashboard di-reset.", "info");
      syncUI(res.state);
      await refreshHistory();
      if (window.resetMapTrack) window.resetMapTrack();
    }
  });

  clearHistoryBtn?.addEventListener("click", async () => {
    const res = await postRace("/api/history/clear");
    if (res.ok) {
      toast("History dihapus.", "info");
      await refreshHistory();
    }
  });
});
