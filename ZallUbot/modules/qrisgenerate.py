import os

import requests
from pyrogram import Client, filters
from ZallUbot import PY

__MODULE__ = "ǫʀɪs ɢᴇɴᴇʀᴀᴛᴏʀ"
__HELP__ = """
<blockquote><b>Bantuan Untuk QRIS Generator</b>

Perintah:
<code>{0}qris [nominal]</code> → Membuat QRIS sesuai nominal yang dimasukkan (Hanya untuk Owner)

Sumber: API KiPay.id.</blockquote></b>
"""

# Data KiPay.id (pengganti OrderKuota / OkeConnect)
# API key project PRODUCTION dari console.kipay.id -> transaksi asli.
# API key project sandbox -> transaksi tes (trx_id diawali "SBX-").
KIPAY_API_KEY = os.getenv("KIPAY_API_KEY", "")  # isi di .env
KIPAY_MODE = os.getenv("KIPAY_MODE", "production").lower()  # isi di .env
KIPAY_BASE = "https://api.kipay.id"

# ID Telegram Owner
OWNER_ID = [int(x) for x in os.getenv("OWNER_ID", "").split() if x]  # dari .env


def _kipay_unwrap(resp_json):
    """Response KiPay bisa langsung object, atau dibungkus 'data'."""
    if isinstance(resp_json, dict) and isinstance(resp_json.get("data"), dict):
        return resp_json["data"]
    return resp_json


@PY.UBOT("qris")
@PY.TOP_CMD
async def _(client, message):
    if message.from_user.id not in OWNER_ID:
        return await message.reply("❌ Anda tidak memiliki izin untuk menggunakan fitur ini!")

    msg = await message.reply("⏳ Sedang memproses QRIS...")

    # Ambil nominal dari pesan
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        return await msg.edit("❌ Format salah! Gunakan: <code>.qris [nominal]</code>")

    NOMINAL = int(args[1])

    if not KIPAY_API_KEY:
        return await msg.edit("❌ KIPAY_API_KEY belum diisi di .env!")

    try:
        # Buat transaksi QRIS di KiPay.id
        response = requests.post(
            f"{KIPAY_BASE}/api/pay/{KIPAY_API_KEY}/transactions",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            json={"amount": NOMINAL, "note": f"QRIS ZALLUBOT Rp{NOMINAL}"},
            timeout=30,
        )

        if response.status_code not in (200, 201):
            return await msg.edit("❌ Gagal membuat QRIS: " + response.text)

        qris_data = _kipay_unwrap(response.json())
        trx_id = str(qris_data.get("trx_id") or "")
        mode = str(qris_data.get("mode") or "").lower()

        # Wajib production: tolak hasil sandbox supaya tidak salah mode
        if KIPAY_MODE == "production" and (mode == "sandbox" or trx_id.startswith("SBX-")):
            return await msg.edit(
                "❌ API key yang dipakai ternyata API key SANDBOX KiPay. "
                "Ganti KIPAY_API_KEY dengan API key project PRODUCTION di console.kipay.id."
            )

        if not trx_id:
            return await msg.edit(f"❌ Response KiPay tidak berisi trx_id: {qris_data}")

        total = int(qris_data.get("amount") or NOMINAL)

        # Ambil gambar QR resmi dari KiPay (image/png)
        qr_response = requests.get(
            f"{KIPAY_BASE}/api/pay/{KIPAY_API_KEY}/transactions/{trx_id}/qr.png",
            headers={"Accept": "image/png"},
            timeout=30,
        )
        if qr_response.status_code != 200 or not qr_response.content:
            return await msg.edit(f"❌ Gagal mengambil gambar QR KiPay (HTTP {qr_response.status_code})")

        qr_filename = f"qris_{NOMINAL}.png"
        with open(qr_filename, "wb") as f:
            f.write(qr_response.content)

        try:
            await message.reply_document(
                qr_filename,
                caption=(
                    f"✅ QRIS Rp{total:,} berhasil dibuat!\n"
                    f"🧾 ID Transaksi: {trx_id}"
                ).replace(",", "."),
            )
        finally:
            if os.path.exists(qr_filename):
                os.remove(qr_filename)
        await msg.delete()

    except Exception as e:
        await msg.edit(f"❌ Error: {str(e)}")
