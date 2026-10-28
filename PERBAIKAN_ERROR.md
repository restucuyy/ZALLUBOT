# Perbaikan Error Install — VERSI FULL

Ini ZALLUBOT V3 **versi FULL** (semua modul lengkap, termasuk blur,
imagee, removebg, stickers) dengan **satu-satunya perubahan** pada hal
yang membuat error. Tidak ada fitur/modul yang dibuang atau diubah.

## Error lama
Saat Start di panel, install gagal di tengah:
`ERROR: Could not install packages due to an OSError: [Errno 28] No space left on device`
lalu `main.py` crash karena dependensi belum lengkap.

## Penyebabnya (hasil audit seluruh kode)
Di `requirements.txt` lama ada paket **hantu**:
- `removebg` — **tidak diimpor oleh satu file pun** di bot ini (modul
  removebg bekerja lewat API remove.bg + requests, bukan paket ini).
  Tapi pip tetap memasang paketnya DAN seluruh pohon dependensinya:
  onnxruntime, scipy, scikit-image, pymatting — total ratusan MB
  unduhan + hasil pasang. Inilah yang menghabiskan ruang sampai giliran
  paket lain (opencv 49,9 MB di screenshot) gagal diunduh.
- `qrcode` — juga tidak diimpor file mana pun lagi sejak QRIS ganti
  KiPay.id (gambar QR sekarang resmi dari KiPay).

## Perbaikannya (hanya ini)
Dua baris paket hantu itu dibuang dari `requirements.txt` (+ komentar
penjelasan). **Selesai.** Karena tidak ada kode yang mengimpornya,
menghapusnya tidak mengubah fitur apa pun:
- opencv + numpy **tetap ada** — memang dipakai modul blur, imagee,
  removebg, stickers. Semua perintahnya tetap jalan.
- Semua 262 file `.py` identik 100% dengan ZALLUBOT V3 biasa
  (sudah diverifikasi dengan diff).
- Tanpa MongoDB (SQLite lokal), QRIS KiPay.id, main.py panel — utuh.

## Cara jalan (panel Pterodactyl Python)
1. Hapus isi server lama termasuk folder `.local` & `.cache` sisa
   install gagal (cache pip lama itu sendiri bisa ratusan MB).
2. Upload ZIP ini / download dari GitHub, extract di File Manager.
3. Buat `.env` dari `sample.env` (API_ID, API_HASH, BOT_TOKEN, OWNER_ID,
   DEVS, KIPAY_API_KEY production).
4. Startup: PY_FILE = `main.py`, Requirements = `requirements.txt`.
5. Start.
