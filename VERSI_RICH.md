# ZALLUBOT — VERSI RICH (Rich Message UI)

Versi ini = **ZALLUBOT V3 FULL FIXED** (versi yang sudah live di panel)
ditambah satu lapisan tampilan baru: **Rich Message** untuk bot pembuat
userbot. Tidak ada fungsi yang berubah — yang berubah hanya cara layar
bot ditampilkan.

## Yang berubah

### 1. File baru: `ZallUbot/core/rich.py`
Lapisan Rich Message (Bot API 10.1):

- `rich_table(title, rows, footer)` — membangun HTML Rich Message:
  judul `<h3>` + `<table bordered striped>` dua kolom
  `INFO | KETERANGAN` (persis gaya tabel pada bot referensi) + footer.
  Semua nilai yang disisipkan di-escape HTML.
- `btn(...)` / `kb(...)` — membangun `reply_markup` Bot API, termasuk
  field `style` tombol Bot API 9.4: `primary` (navigasi utama),
  `success` (konfirmasi / beli), `danger` (batal / hapus / restart).
- `rich_send(...)` — POST `sendRichMessage` ke
  `https://api.telegram.org/bot<token>/...` memakai `BOT_TOKEN` dan
  session aiohttp bersama (`aiosession`).
- `rich_edit(...)` — `editMessageText` dengan parameter `rich_message`.
- Helper untuk handler Pyrogram (semua dengan **fallback otomatis** ke
  tampilan klasik bila rich gagal / dimatikan):
  - `reply_rich(message, ...)` — pesan baru (fallback `reply_text`).
  - `send_rich(client, chat_id, ...)` — kirim ke chat (fallback `send_message`).
  - `edit_rich_message(message, ...)` — edit pesan (fallback `edit_text`).
  - `edit_rich_query(query, ...)` — edit dari callback: coba rich edit →
    bila gagal (mis. pesan foto dari `/start` tidak bisa diedit teksnya
    lewat Bot API) kirim Rich Message baru lalu hapus pesan lama →
    fallback terakhir `edit_text` klasik.
- Kit layar ZALLUBOT: `home_table()`, `start_buttons()`,
  `payment_table()`, `payment_buttons()` — isi & callback-nya mirror
  persis `MSG.START` / `BTN.START` / `MSG.TEXT_PAYMENT` / `BTN.PLUS_MINUS`.

### 2. Layar bot yang diganti ke rich (tabel + tombol berwarna)
Semua `callback_data`, urutan langkah, dan logika handler **sama persis**
dengan sebelumnya; hanya presentasinya yang diganti:

- `ZallUbot/modules/add_ubot.py`
  - Callback `bahan` (sudah punya userbot / slot penuh / belum premium /
    premium) → tabel status + tombol Restart (danger) / Lanjutkan
    (success) / Kembali (primary).
  - Callback `status` → tabel STATUS / PREFIX / EXPIRED bermerek
    ZALLUBOT (kredit lama `@yaetiem` diganti merek ZALLUBOT; tombol
    "ᴋᴇᴍʙᴀʟɪ" yang memakai aksara 卍/卐 dinormalkan ke "⦪ ᴋᴇᴍʙᴀʟɪ ⦫").
  - Callback `buat_ubot` (semua cabangnya).
  - Callback `bayar_dulu` → tabel pembayaran (mirror `TEXT_PAYMENT`,
    nilai sama: 30/30/1) + tombol +/- , Konfirmasi (success),
    Batalkan (danger).
  - Layar "Berhasil diaktifkan" di akhir pembuatan userbot + pesan log
    ke `LOGS_MAKER_UBOT`.
  - Perintah `control`, hasil `ress_ubot`, hasil perintah `restart`.
  - Layar admin list userbot: `cek_ubot`/`getubot`, pager `p_ub`/`n_ub`,
    dan tampilan setelah `del_ubot` + pemberitahuan masa aktif habis.
- `ZallUbot/modules/payment.py`
  - Callback `home` → layar utama rich (tabel home + menu utama
    berstyle, isi mirror `MSG.START`/`BTN.START`).
  - Callback `kurang`/`tambah` → tabel pembayaran diperbarui via rich.
  - Callback `confirm`: layar "tidak dapat diproses" dan "bukti
    terkirim" (tombol kontak owner tetap URL yang sama).
  - Callback `success`/`failed`: pemberitahuan ke pengguna + hasil
    penambahan premium.
- Kredit/penulis pada teks bot yang disentuh diganti menjadi merek
  **ZALLUBOT** (judul tabel "🛡️ ZALLUBOT", footer "© ZALLUBOT").

### 3. Toggle di config
- `config.py` + `sample.env`: variabel baru **`RICH_MESSAGES`**
  (default `on`). Isi `off` di `.env` untuk mematikan rich sepenuhnya —
  semua layar otomatis kembali ke tampilan klasik Pyrogram.

## Batasan penting Rich Message

- Rich Message adalah fitur **Bot API** — hanya pesan dari **BOT**
  (akun bot dengan token) yang bisa rich. Akun **userbot** (Pyrogram /
  MTProto) **tidak bisa** mengirim rich message, jadi seluruh modul
  perintah userbot (230+ modul `.qris`, `.ping`, dll) **tetap klasik**
  dan tidak disentuh sama sekali.
- Layar `/start` pertama tetap klasik (foto + caption) karena caption
  media tidak bisa dikonversi ke rich; begitu pengguna menekan tombol
  menu pertama, layar berikutnya tampil rich (helper mengganti pesan
  foto itu dengan Rich Message baru dan menghapus yang lama).
- Prompt percakapan (minta nomor HP, OTP, password 2FA) tetap klasik
  karena itu input percakapan, bukan layar menu.
- Salinan bukti pembayaran foto ke owner (`pesan.copy` + keyboard
  `BTN.ADD_EXP`) tetap klasik — itu pesan media milik alur persetujuan
  owner dan tidak aman dikonversi.

## Yang TIDAK berubah (identik dengan FULL FIXED)

- Database lokal SQLite (`data/zallubot.db`) — tetap tanpa MongoDB.
- Integrasi **KiPay.id** di `ZallUbot/modules/qrisgenerate.py` —
  **tidak diubah sama sekali**. Sudah diverifikasi terhadap dokumentasi
  resmi https://kipay.id/docs/api (28 Okt 2026): endpoint
  `POST /api/pay/{apiKey}/transactions`, gambar QR
  `GET .../transactions/{trxId}/qr.png`, nominal akhir dari field
  `amount` pada response, dan penolakan hasil sandbox (`SBX-` /
  `mode: sandbox`) saat `KIPAY_MODE=production` — semuanya sesuai.
- Launcher panel `main.py` (persiapan event loop uvloop + PATH
  `/home/container/node/bin`) — sama.
- `requirements.txt` slim (`Pillow>=10.4.0`, tanpa paket `removebg` /
  `qrcode`) — sama.
- Seluruh modul userbot dan file lain di luar daftar di atas — sama
  persis (lihat diff terhadap `zallubot-full-fixed`).
