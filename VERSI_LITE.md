# ZALLUBOT V3 — VERSI LITE (untuk panel yang gagal install karena disk)

Isi paket ini SAMA dengan ZALLUBOT V3 (tanpa MongoDB + KiPay.id + panel
Pterodactyl), hanya install-nya dibuat jauh lebih ringan karena versi
penuh gagal diinstall di panel dengan error
`[Errno 28] No space left on device`.

## Yang dibuang (dan kenapa aman)

Dari `requirements.txt`:
- `opencv-python-headless` — unduhan 49,9 MB, terpasang 100+ MB.
  Hanya dipakai 4 modul di bawah.
- `numpy` — tidak diimpor langsung oleh modul mana pun (cuma kebutuhan opencv).
- `removebg` (paket pip) — **tidak diimpor oleh satu file pun** di bot ini,
  tapi pip memasang dependensinya yang raksasa: onnxruntime, scipy,
  scikit-image (total ratusan MB) untuk sesuatu yang tidak pernah dipakai.
- `qrcode` — tidak diimpor lagi sejak modul qris ganti KiPay
  (QR sekarang diambil sebagai gambar resmi dari KiPay).

Dari folder modul (terpaksa dibuang karena bot mengimpor SEMUA modul saat
start — kalau file-nya ada tapi opencv tidak terpasang, bot crash):
- `blur.py` — perintah `.blur`
- `imagee.py` — perintah `.mirror`, `.negative`, dll.
- `removebg.py` — perintah `.rmbg`
- `stickers.py` — perintah `.q`, `.kang`, `.tiny`, `.mmf`

Total hemat unduhan + ruang terpasang: ratusan MB.
**Semua fitur lain tetap**: pembuat userbot, 250+ modul lain, database
lokal SQLite, dan `.qris` KiPay.id berfungsi penuh.

## Cara pakai
Sama seperti V3 biasa (lihat README.md): hapus dulu isi server lama
termasuk folder `.local` dan `.cache` sisa install gagal, upload ZIP ini,
extract, buat `.env`, Startup PY_FILE = `main.py`, lalu Start.
