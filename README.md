# SprintDash

SprintDash adalah dashboard race tracker berbasis Flask dengan desain dark-neon seperti mockup.

## Fitur
- Target distance
- Ambil lokasi via browser GPS
- Start / stop / reset
- Realtime distance, speed, time, status
- Progress ring
- Peta jalur realtime
- History run tersimpan ke SQLite
- Siap deploy dengan Gunicorn

## Struktur
Sesuai struktur modular yang kamu minta:
- `app/routes/`
- `app/services/`
- `app/utils/`
- `app/models/`
- `app/templates/`
- `app/static/`
- `tests/`

## Run lokal
```bash
pip install -r requirements.txt
python app.py
```

## Deploy
Project ini sudah disiapkan untuk hosting berbasis Python dengan Gunicorn.
Di Render:
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn wsgi:app`

## Catatan
- GPS realtime memakai browser geolocation.
- History tersimpan ke SQLite.
- Untuk produksi, jalankan di HTTPS agar geolocation aktif di browser.
