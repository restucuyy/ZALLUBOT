# Perbaikan Error Install (No space left on device)

Repo ini = ZALLUBOT V3 (tanpa MongoDB, QRIS KiPay.id, jalan di panel
Pterodactyl Python) yang **penyebab error install-nya sudah dibenahi**.

## Error lama
Saat Start di panel, pip gagal di tengah:
`ERROR: Could not install packages due to an OSError: [Errno 28] No space left on device`
lalu `main.py` crash karena dependensi belum lengkap.

## Penyebabnya
`requirements.txt` versi lama memuat paket-paket raksasa:
- `opencv-python-headless` — unduhan 49,9 MB (paket yang gagal di screenshot),
  terpasang 100+ MB. Hanya dipakai 4 modul.
- `removebg` (paket pip) — **tidak diimpor oleh satu file pun** di bot ini,
  tapi menarik dependensi raksasa: onnxruntime, scipy, scikit-image
  (total ratusan MB) untuk fitur yang tidak pernah dipakai.
- `numpy` — tidak diimpor langsung oleh modul mana pun.
- `qrcode` — tidak diimpor lagi sejak QRIS ganti KiPay.id.

## Yang dibenahi di repo ini
- 4 paket di atas dibuang dari `requirements.txt`.
- 4 modul pemakai opencv dibuang (bot mengimpor SEMUA modul saat start,
  jadi file-nya harus ikut dibuang): `blur.py`, `imagee.py`, `removebg.py`,
  `stickers.py`. Perintah yang hilang hanya: `.blur`, `.mirror`, `.negative`,
  `.rmbg`, `.q`, `.kang`, `.tiny`, `.mmf`.
- Selain itu **tidak ada yang berubah**: database lokal SQLite
  (`data/zallubot.db`), `.qris` KiPay.id, dan 250+ modul lain utuh.

## Cara jalan (panel Pterodactyl Python)
1. Hapus isi server lama termasuk folder `.local` & `.cache`.
2. Download repo ini (Code → Download ZIP) atau upload ulang ZIP-nya,
   extract di File Manager.
3. Buat `.env` dari `sample.env` (API_ID, API_HASH, BOT_TOKEN, OWNER_ID,
   DEVS, KIPAY_API_KEY production).
4. Startup: PY_FILE / App Py File = `main.py`, Requirements = `requirements.txt`.
5. Start.

## Catatan file storage
Folder `storage/` berisi 4 file biner (2 font .ttf, template.jpg,
TM_BLACK.png) yang dipakai beberapa modul gambar/teks. Pastikan keempat
file itu ikut ter-upload ke panel bersama kodenya.
