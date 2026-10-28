# ZALLUBOT V2 — Catatan Perbaikan

## Rebranding
- Package `PyroUbot` → `ZallUbot` di **semua** file (folder, 306 referensi
  import/string, `start.sh`, perintah jalan sekarang `python3 -m ZallUbot`).
- Kredit tampil "©akbarbotz1" di modul newgcast → "©ZALLUBOT".
- Tulisan console "MAKRICO" di core/function/plugins.py → "ZALLUBOT".
- 3 file duplikat basi tanpa ekstensi .py di modules/ (brat, cecan, tiktok —
  versi lamanya, masih ber-import PyroUbot dan tidak pernah dimuat loader)
  dibuang; versi .py resminya tetap ada.
- README ditulis ulang untuk ZALLUBOT.

## Keamanan (penting!)
Zip sumber membawa kredensial asli owner lama. Semuanya sudah dibersihkan:
- `config.py` & `sample.env`: default `BOT_TOKEN`, `API_HASH`, `RMBG_API`,
  dan `MONGO_URL` (berisi username+password MongoDB Atlas) milik owner lama
  dihapus — sekarang wajib dari `.env` sendiri.
- `modules/qrisgenerate.py`: `MERCHANT_ID`, `API_KEY` OkeConnect, dan string
  QRIS statis toko owner lama ("ALFASEFY STORE, MAGETAN") dihapus → dibaca
  dari `.env` (`QRIS_MERCHANT_ID`, `QRIS_API_KEY`, `QRIS_CODE`).
  `OWNER_ID` modul ini juga sekarang dari `.env`, bukan ID hardcoded.
- `modules/subdocreate.py`: API token Cloudflare asli + zone ID/domain
  owner lama dihapus → token dari `.env`, `DOMAIN_LIST` dikosongkan.
- `cookies.txt` (cookies YouTube milik orang lain) dibuang dari paket.
- Folder `.git` bawaan dibuang; `.gitignore` ditambahkan
  (`.env`, `*.session`, `cookies.txt`, dll).

## Bug yang diperbaiki
- `__main__.py`: handler TimeoutError memakai kunci dict yang tidak ada
  (`_ubot["xzhee"]`) sehingga pasti KeyError saat ada userbot timeout —
  diperbaiki menjadi `_ubot["name"]` (sesuai kunci dari `get_userbots()`).
- `__main__.py`: lambda handler signal menangkap variabel loop secara
  late-binding — diperbaiki (`lambda s=s: ...`).
- `core/helpers/anim_tool.py`: 2 string dengan invalid escape sequence
  (`\)`, `\(`) yang menimbulkan SyntaxWarning — diperbaiki.

## Dependensi
- Duplikat di `requirements.txt` dibuang (pySmartDL ×2, python-dotenv ×2,
  httpx[http2] ×2 dengan pin bertabrakan → disisakan `==0.27.2`).
- Modul memakai tapi tidak ada di requirements (pasti ModuleNotFoundError
  saat modul dimuat) — ditambahkan: `geopy` (gps), `pytimeparse` (remind),
  `qrcode` (qrisgenerate), `speedtest-cli` (ping2).

## Verifikasi
- Semua 261 file `.py`: `py_compile` bersih, 0 error.
- Semua import internal `ZallUbot.*`: terverifikasi mengarah ke modul yang ada.
