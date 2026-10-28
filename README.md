# ZALLUBOT — Tanpa MongoDB + KiPay.id + Panel Pterodactyl

Userbot Telegram berbasis **Pyrogram** (Python) dengan 200+ modul.
Versi ini sama persis dengan ZALLUBOT V2 (semua modul, perintah, dan
fitur **tidak diubah**), kecuali 3 hal yang diminta:

1. **Tanpa MongoDB** — database diganti SQLite lokal `data/zallubot.db`
   (dibuat otomatis, tanpa URL, tanpa server, tanpa daftar MongoDB Atlas).
2. **QRIS OrderKuota / OkeConnect dihapus, diganti KiPay.id** —
   perintahnya tetap sama: `.qris [nominal]` (khusus Owner).
3. **Jalan via Panel Pterodactyl Python** — ada file `main.py` sebagai
   file utama panel.

**Author: ZALLUBOT**
Base: fork dari PyroUbot (userbot Pyrogram).

## Cara jalan di Panel Pterodactyl (egg Python)

1. Buat server baru dengan **egg Python** di panel kamu.
2. Upload file ZIP ini ke **File Manager**, lalu **Extract / Unarchive**
   sampai file `main.py`, `sample.env`, `requirements.txt`, dan folder
   `ZallUbot` ada di **folder paling luar** (bukan di dalam folder lain).
3. Buat file `.env` (salin isi `sample.env`) lalu isi data kamu sendiri:
   - `API_ID` & `API_HASH` dari my.telegram.org
   - `BOT_TOKEN` dari @BotFather
   - `OWNER_ID` & `DEVS` = ID Telegram kamu
   - `KIPAY_API_KEY` = API key KiPay.id (lihat bawah) — hanya untuk `.qris`
   - **Tidak ada lagi `MONGO_URL`** — memang sudah dihapus.
4. Di menu **Startup** panel, isi:
   - **App Py File / PY_FILE:** `main.py`
   - **Requirements File** (kalau ada kolomnya): `requirements.txt`
5. Klik **Start**. Panel akan memasang `requirements.txt` lalu menjalankan
   bot. Bot pembuat userbot (dari `BOT_TOKEN`) akan online di Telegram.

> Kalau egg panel kamu tidak otomatis memasang requirements, jalankan
> sekali dari Console / terminal panel: `pip3 install -r requirements.txt`
> lalu Start lagi.

## Database lokal (pengganti MongoDB)

- Semua data (userbot, prefix, variabel, masa aktif, antigcast) disimpan
  di **`data/zallubot.db`**.
- **Backup / pindah panel:** cukup unduh & salin file itu. Jangan hapus
  folder `data/` kalau tidak mau data userbot hilang.
- File ini **tidak** disertakan di ZIP — akan dibuat sendiri saat bot
  pertama kali jalan.

## QRIS pakai KiPay.id (pengganti OrderKuota)

- Daftar & buat project di **console.kipay.id**, ambil **API key project
  PRODUCTION** (untuk transaksi asli), isi ke `.env`:
  `KIPAY_API_KEY = ...` dan `KIPAY_MODE = production`
- Perintah tetap: `.qris 10000` di userbot (khusus Owner) → bot membuat
  transaksi KiPay, mengambil gambar QR resmi dari KiPay, dan mengirimnya.
- Kalau API key yang terpasang ternyata key **sandbox** (transaksi
  `SBX-...`), bot menolak dan memberi tahu — supaya tidak salah mode jualan.
- Integrasi lama `gateway.okeconnect.com` / OrderKuota (`QRIS_MERCHANT_ID`,
  `QRIS_API_KEY`, `QRIS_CODE`) **sudah dihapus total**.

## Cara jalan di VPS (tetap bisa, seperti V2)

```bash
apt update && apt upgrade -y
apt install ffmpeg -y
bash installnode.sh
apt install python3.10-venv -y
python3 -m venv venv && source venv/bin/activate
pip3 install -r requirements.txt
cp sample.env .env && nano .env
python3 -m ZallUbot
# atau: python3 main.py
```

Detail semua perubahan ada di [CHANGELOG_V3.md](CHANGELOG_V3.md).
