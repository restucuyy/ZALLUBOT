# ZALLUBOT — Changelog: Tanpa MongoDB + KiPay.id + Panel Pterodactyl

Basis: ZALLUBOT V2. **Semua modul, perintah, dan fitur lain TIDAK diubah.**
File `.py` yang berubah hanya 3, ditambah 1 file baru (`main.py`):

## 1. MongoDB dibuang, diganti database lokal SQLite
- `ZallUbot/core/database/__init__.py` ditulis ulang: dulu membuat koneksi
  MongoDB Atlas via `motor` (`AsyncIOMotorClient(MONGO_URL)`), sekarang
  memakai **SQLite bawaan Python** di file `data/zallubot.db`.
- API-nya meniru persis API motor yang dipakai file lain (`find_one`,
  `find` + `async for`, `update_one` dengan `$set`/`$unset` kunci bertitik,
  `$exists`, akses `db["koleksi"]`, `db.koleksi`, sub-koleksi), jadi
  `variabel.py`, `userbot.py`, `pref.py`, `expired.py`, `antigcast.py`, dan
  modul `antigcast.py` **tidak perlu diubah satu baris pun** — variabel
  `mongo_client` / `mongodb` yang mereka impor sekarang menunjuk ke
  database lokal.
- Tipe data yang disimpan modul tetap utuh: string, angka, list, dict
  (contoh AFK), dan `datetime` ber-timezone (masa aktif / expired) —
  sudah diuji bolak-balik (round-trip) sama persis.
- `config.py` & `sample.env`: `MONGO_URL` dihapus. Ada `DB_PATH` opsional
  (default `data/zallubot.db`).
- `requirements.txt`: `motor`, `pymongo`, `dnspython` dibuang.
- Backup / pindah panel = salin file `data/zallubot.db` saja.

## 2. QRIS OrderKuota / OkeConnect dihapus, diganti KiPay.id
- `ZallUbot/modules/qrisgenerate.py` ditulis ulang ke KiPay.id
  (dokumentasi resmi https://kipay.id/docs/api):
  - Buat transaksi: `POST https://api.kipay.id/api/pay/{KIPAY_API_KEY}/transactions`
  - Gambar QR resmi: `GET .../transactions/{trx_id}/qr.png`
  - Perintah & izin **tetap sama**: `.qris [nominal]`, khusus Owner.
  - Total yang ditampilkan memakai field `amount` dari KiPay (bisa
    termasuk kode unik), lengkap dengan ID transaksi.
  - `KIPAY_MODE=production` (default) **menolak** hasil sandbox
    (`SBX-...` / mode sandbox) seperti bot KiPay sebelumnya.
- Endpoint lama `gateway.okeconnect.com` dan env `QRIS_MERCHANT_ID` /
  `QRIS_API_KEY` / `QRIS_CODE` **dihapus total**; env baru:
  `KIPAY_API_KEY`, `KIPAY_MODE`.
- Modul `payment.py` (pembayaran manual ke DANA owner + konfirmasi admin)
  **tidak** memakai OrderKuota, jadi tidak diubah.

## 3. Jalan via Panel Pterodactyl Python
- File baru `main.py` di folder terluar: menjalankan bot persis seperti
  `python3 -m ZallUbot` (`runpy.run_module`). Di panel, isi
  **App Py File / PY_FILE = `main.py`** dan Requirements = `requirements.txt`.
- `README.md` ditulis ulang dengan langkah panel + VPS.
- `.gitignore`: folder `data/` & `*.db` ditambahkan.

## Verifikasi
- Semua 262 file `.py`: `py_compile` bersih, 0 error.
- Smoke test database lokal: set/get/hapus vars (dotted), dict AFK,
  list vars, tambah/hapus userbot + `find($exists)`, prefix list,
  expired datetime Asia/Jakarta, antigcast — **semua lulus**, dan perilaku
  tepinya sama dengan Mongo asli (mis. `get_pref` setelah `rem_pref`).
- Smoke test KiPay (API ditiru/mock): endpoint, nominal, total dari
  response, unduh `qr.png`, kirim dokumen, file sementara dibersihkan —
  **lulus**. Transaksi asli tetap butuh `KIPAY_API_KEY` production milikmu.
- Diff terhadap V2: hanya file-file di atas yang berbeda; 258 file `.py`
  lain identik 100%.
