import asyncio
from datetime import datetime

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone

from ZallUbot import *
from ZallUbot.core.rich import (
    btn,
    edit_rich_query,
    home_table,
    payment_buttons,
    payment_table,
    send_rich,
    start_buttons,
)

CONFIRM_PAYMENT = []


@PY.CALLBACK("^confirm")
async def _(client, callback_query):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    get = await bot.get_users(user_id)
    CONFIRM_PAYMENT.append(get.id)
    try:
        await callback_query.message.delete()
        pesan = await bot.ask(
            user_id,
            f"""
<blockquote><b>SILAHKAN MELAKUKAN PEMBAYARAN KE NOMOR DANA OWNER</b>           

DANA : ||HUB. OWNER||

<b>💬 sɪʟᴀʜᴋᴀɴ ᴋɪʀɪᴍᴋᴀɴ ʙᴜᴋᴛɪ sᴄʀᴇᴇɴsʜᴏᴛ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴀɴᴅᴀ: {full_name}</b></blockquote>
""",
            timeout=300,
        )
    except asyncio.TimeoutError as out:
        return await bot.send_message(get.id, "ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪs")
    if get.id in CONFIRM_PAYMENT:
        if not pesan.photo:
            CONFIRM_PAYMENT.remove(get.id)
            return await send_rich(
                bot,
                user_id,
                "🛡️ ZALLUBOT",
                [
                    ("STATUS", "❌ Tidak dapat diproses"),
                    ("INFO", "Harap kirimkan screenshot bukti pembayaran Anda yang valid"),
                    ("PETUNJUK", "Silakan konfirmasi ulang pembayaran Anda"),
                ],
                buttons=[
                    [btn("✅ ᴋᴏɴꜰɪʀᴍᴀsɪ", callback_data="confirm", style="success")],
                ],
            )
        elif pesan.photo:
            buttons = BTN.ADD_EXP(get.id)
            await pesan.copy(
                OWNER_ID,
                reply_markup=buttons,
            )
            CONFIRM_PAYMENT.remove(get.id)
            return await send_rich(
                bot,
                user_id,
                "🛡️ ZALLUBOT",
                [
                    ("STATUS", "✅ Bukti pembayaran terkirim"),
                    ("INFO", f"Baik {full_name}, silakan ditunggu dan jangan spam ya"),
                    ("KONFIRMASI", "Pembayaran Anda akan dikonfirmasi setelah 1-2 jam kerja"),
                ],
                buttons=[
                    [btn("📞 ᴏᴡɴᴇʀ", url="https://t.me/yaetiem")],
                ],
            )


@PY.CALLBACK("^(kurang|tambah)")
async def _(client, callback_query):
    BULAN = int(callback_query.data.split()[1])
    HARGA = 20
    QUERY = callback_query.data.split()[0]
    try:
        if QUERY == "kurang":
            if BULAN > 1:
                BULAN -= 1
                TOTAL_HARGA = HARGA * BULAN
        elif QUERY == "tambah":
            if BULAN < 12:
                BULAN += 1
                TOTAL_HARGA = HARGA * BULAN
        title, rows, footer = payment_table(HARGA, TOTAL_HARGA, BULAN)
        await edit_rich_query(
            callback_query,
            title,
            rows,
            buttons=payment_buttons(BULAN, callback_query.from_user.id),
            footer=footer,
        )
    except:
        pass


@PY.CALLBACK("^(success|failed|home)")
async def _(client, callback_query):
    query = callback_query.data.split()
    get_user = await bot.get_users(query[1])
    if query[0] == "success":
        await send_rich(
            bot,
            get_user.id,
            "🛡️ ZALLUBOT",
            [
                ("STATUS", "✅ Pembayaran Anda berhasil dikonfirmasi"),
                ("INFO", "Sekarang Anda bisa membuat userbot"),
            ],
            buttons=[
                [btn("🔥 ʙᴜᴀᴛ ᴜꜱᴇʀʙᴏᴛ 🔥", callback_data="buat_ubot", style="success")],
            ],
        )
        await add_to_vars(client.me.id, "PREM_USERS", get_user.id)
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(query[2]))
        await set_expired_date(get_user.id, expired)
        return await edit_rich_query(
            callback_query,
            "🛡️ ZALLUBOT",
            [
                ("STATUS", "✅ Ditambahkan ke anggota premium"),
                ("PENGGUNA", f"{get_user.first_name} {get_user.last_name or ''}".strip()),
            ],
        )
    if query[0] == "failed":
        await send_rich(
            bot,
            get_user.id,
            "🛡️ ZALLUBOT",
            [
                ("STATUS", "❌ Pembayaran Anda tidak bisa dikonfirmasi"),
                ("INFO", "Silakan lakukan pembayaran dengan benar"),
            ],
            buttons=[
                [btn("💳 ʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ 💳", callback_data="bayar_dulu", style="success")],
            ],
        )
        return await edit_rich_query(
            callback_query,
            "🛡️ ZALLUBOT",
            [
                ("STATUS", "❌ Tidak ditambahkan ke anggota premium"),
                ("PENGGUNA", f"{get_user.first_name} {get_user.last_name or ''}".strip()),
            ],
        )
    if query[0] == "home":
        if get_user.id in CONFIRM_PAYMENT:
            CONFIRM_PAYMENT.remove(get_user.id)
        title, rows, footer = home_table(
            callback_query.from_user.first_name,
            callback_query.from_user.last_name,
            client.me.username,
            len(ubot._ubot),
        )
        return await edit_rich_query(
            callback_query,
            title,
            rows,
            buttons=start_buttons(callback_query.from_user.id),
            footer=footer,
        )
