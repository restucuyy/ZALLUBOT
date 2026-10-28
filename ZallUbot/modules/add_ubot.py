import asyncio
import importlib
from datetime import datetime

from pyrogram.enums import SentCodeType
from pyrogram.errors import *
from pyrogram.types import *
from pyrogram.raw import functions

from ZallUbot import *
from ZallUbot.core.rich import (
    btn,
    edit_rich_message,
    edit_rich_query,
    payment_buttons,
    payment_table,
    reply_rich,
    send_rich,
)


@PY.BOT("start")
@PY.START
@PY.PRIVATE
async def _(client, message):
    user_id = message.from_user.id
    buttons = BTN.START(message)
    msg = MSG.START(message)
    pantek = "https://files.catbox.moe/7ggxo2.jpg"

    await bot.send_photo(
        user_id, 
        pantek, 
        caption=msg, 
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else None
    )


@PY.CALLBACK("bahan")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        return await edit_rich_query(
            callback_query,
            "🛡️ ZALLUBOT",
            [
                ("STATUS", "✅ Userbot sudah dibuat"),
                (
                    "INFO",
                    "Jika userbot Anda tidak bisa digunakan, silakan tekan tombol Restart di bawah",
                ),
            ],
            buttons=[
                [btn("⦪ ʀᴇꜱᴛᴀʀᴛ ⦫", callback_data="ress_ubot", style="danger")],
                [btn("⦪ ᴋᴇᴍʙᴀʟɪ ⦫", callback_data=f"home {user_id}", style="primary")],
            ],
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        return await edit_rich_query(
            callback_query,
            "🛡️ ZALLUBOT",
            [
                ("STATUS", "❌ Tidak bisa membuat userbot"),
                ("MAKSIMAL", f"{len(ubot._ubot)} userbot telah tercapai"),
                ("INFO", "Silakan hubungi owner"),
            ],
            buttons=[
                [btn("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}", style="primary")],
            ],
        )
    premium_users, ultra_premium_users = await get_list_from_vars(client.me.id, "PREM_USERS"), await get_list_from_vars(client.me.id, "ULTRA_PREM")
    if user_id not in premium_users and user_id not in ultra_premium_users:
        return await edit_rich_query(
            callback_query,
            "🛡️ ZALLUBOT",
            [
                ("STATUS", "💎 Belum Premium"),
                (
                    "INFO",
                    "Anda belum membeli userbot — lanjutkan untuk melihat pembayaran",
                ),
                ("BANTUAN", "Jika ada kendala, silakan hubungi owner bot"),
            ],
            buttons=[
                [btn("⦪ ʟᴀɴᴊᴜᴛᴋᴀɴ ⦫", callback_data="bayar_dulu", style="success")],
                [btn("⦪ ᴋᴇᴍʙᴀʟɪ ⦫", callback_data=f"home {user_id}", style="primary")],
            ],
        )
    else:
        return await edit_rich_query(
            callback_query,
            "🛡️ ZALLUBOT",
            [
                ("STATUS", "✅ Premium"),
                (
                    "INFO",
                    "Anda telah membeli userbot — silakan pencet tombol Lanjutkan untuk membuat userbot",
                ),
            ],
            buttons=[
                [btn("⦪ ʟᴀɴᴊᴜᴛᴋᴀɴ ⦫", callback_data="buat_ubot", style="success")],
            ],
        )


@PY.CALLBACK("status")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        exp = await get_expired_date(user_id)
        prefix = await get_pref(user_id)
        waktu = exp.strftime("%d-%m-%Y") if exp else "None"
        return await edit_rich_query(
            callback_query,
            "🛡️ ZALLUBOT — STATUS",
            [
                ("STATUS", "Premium"),
                ("PREFIX", prefix[0]),
                ("EXPIRED", waktu),
            ],
            buttons=[
                [btn("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}", style="primary")],
            ],
        )
    else:
        return await edit_rich_query(
            callback_query,
            "🛡️ ZALLUBOT — STATUS",
            [
                ("STATUS", "❌ Belum membeli userbot"),
                (
                    "INFO",
                    "Maaf, Anda belum membeli userbot — silakan membeli terlebih dahulu",
                ),
            ],
            buttons=[
                [btn("✮ ʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ ✮", callback_data="bahan", style="success")],
                [btn("⦪ ᴋᴇᴍʙᴀʟɪ ⦫", callback_data=f"home {user_id}", style="primary")],
            ],
        )


@PY.CALLBACK("buat_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id in ubot._get_my_id:
        return await edit_rich_query(
            callback_query,
            "🛡️ ZALLUBOT",
            [
                ("STATUS", "✅ Userbot sudah dibuat"),
                (
                    "INFO",
                    "Jika userbot Anda tidak bisa digunakan, silakan tekan tombol Restart di bawah",
                ),
            ],
            buttons=[
                [btn("⦪ ʀᴇꜱᴛᴀʀᴛ ⦫", callback_data="ress_ubot", style="danger")],
                [btn("⦪ ᴋᴇᴍʙᴀʟɪ ⦫", callback_data=f"home {user_id}", style="primary")],
            ],
        )
    elif len(ubot._ubot) + 1 > MAX_BOT:
        return await edit_rich_query(
            callback_query,
            "🛡️ ZALLUBOT",
            [
                ("STATUS", "❌ Tidak bisa membuat userbot"),
                ("MAKSIMAL", f"{len(ubot._ubot)} userbot telah tercapai"),
                ("INFO", "Silakan hubungi admin jika mau dibuatkan bot seperti saya"),
            ],
            buttons=[
                [btn("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}", style="primary")],
            ],
        )
    premium_users, ultra_premium_users = await get_list_from_vars(client.me.id, "PREM_USERS"), await get_list_from_vars(client.me.id, "ULTRA_PREM")
    if user_id not in premium_users and user_id not in ultra_premium_users:
        return await edit_rich_query(
            callback_query,
            "🛡️ ZALLUBOT",
            [
                ("STATUS", "❌ Belum membeli userbot"),
                (
                    "INFO",
                    "Maaf, Anda belum membeli userbot — silakan membeli terlebih dahulu",
                ),
            ],
            buttons=[
                [btn("⦪ ʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ ⦫", callback_data="bahan", style="success")],
                [btn("⦪ ᴋᴇᴍʙᴀʟɪ ⦫", callback_data=f"home {user_id}", style="primary")],
            ],
        )
    else:
        return await edit_rich_query(
            callback_query,
            "🛡️ ZALLUBOT",
            [
                ("STATUS", "✅ Premium"),
                ("BAHAN", "Phone Number — nomor HP akun Telegram"),
                ("INFO", "Jika sudah tersedia, silakan klik tombol di bawah"),
            ],
            buttons=[
                [btn("⦪ ʟᴀɴᴊᴜᴛᴋᴀɴ ⦫", callback_data="add_ubot", style="success")],
            ],
        )

@PY.CALLBACK("bayar_dulu")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    title, rows, footer = payment_table(30, 30, 1)
    return await edit_rich_query(
        callback_query,
        title,
        rows,
        buttons=payment_buttons(1, user_id),
        footer=footer,
    )


@PY.CALLBACK("add_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.message.delete()
    try:
        phone = await bot.ask(
            user_id,
            (
                "<b>✮ sɪʟᴀʜᴋᴀɴ ᴍᴀsᴜᴋᴋᴀɴ ɴᴏᴍᴏʀ ᴛᴇʟᴇᴘᴏɴ ᴛᴇʟᴇɢʀᴀᴍ ᴀɴᴅᴀ ᴅᴇɴɢᴀɴ ꜰᴏʀᴍᴀᴛ ᴋᴏᴅᴇ ɴᴇɢᴀʀᴀ.\nᴄᴏɴᴛᴏʜ: +628xxxxxxx</b>\n"
                "\n<b>✮ ɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "<blockquote>✮ ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪꜱ!\n✮ ɢᴜɴᴀᴋᴀɴ /ꜱᴛᴀʀᴛ ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>")
    if await is_cancel(callback_query, phone.text):
        return
    phone_number = phone.text
    new_client = Ubot(
        name=str(callback_query.id),
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=False,
    )
    get_otp = await bot.send_message(user_id, "<blockquote><b>✮ ᴍᴇɴɢɪʀɪᴍ ᴋᴏᴅᴇ ᴏᴛᴘ...</b></blockquote>")
    await new_client.connect()
    try:
        code = await new_client.send_code(phone_number.strip())
    except ApiIdInvalid as AID:
        await get_otp.delete()
        return await bot.send_message(user_id, AID)
    except PhoneNumberInvalid as PNI:
        await get_otp.delete()
        return await bot.send_message(user_id, PNI)
    except PhoneNumberFlood as PNF:
        await get_otp.delete()
        return await bot.send_message(user_id, PNF)
    except PhoneNumberBanned as PNB:
        await get_otp.delete()
        return await bot.send_message(user_id, PNB)
    except PhoneNumberUnoccupied as PNU:
        await get_otp.delete()
        return await bot.send_message(user_id, PNU)
    except Exception as error:
        await get_otp.delete()
        return await bot.send_message(user_id, f"ERROR: {error}")
    try:
        sent_code = {
            SentCodeType.APP: "<a href=tg://openmessage?user_id=777000>ᴀᴋᴜɴ ᴛᴇʟᴇɢʀᴀᴍ</a> ʀᴇsᴍɪ",
            SentCodeType.SMS: "sᴍs ᴀɴᴅᴀ",
            SentCodeType.CALL: "ᴘᴀɴɢɢɪʟᴀɴ ᴛᴇʟᴘᴏɴ",
            SentCodeType.FLASH_CALL: "ᴘᴀɴɢɢɪʟᴀɴ ᴋɪʟᴀᴛ ᴛᴇʟᴇᴘᴏɴ",
            SentCodeType.FRAGMENT_SMS: "ꜰʀᴀɢᴍᴇɴᴛ sᴍs",
            SentCodeType.EMAIL_CODE: "ᴇᴍᴀɪʟ ᴀɴᴅᴀ",
        }
        await get_otp.delete()
        otp = await bot.ask(
            user_id,
            (
                "<b>✮ sɪʟᴀᴋᴀɴ ᴘᴇʀɪᴋsᴀ ᴋᴏᴅᴇ ᴏᴛᴘ ᴅᴀʀɪ ᴀᴋᴜɴ ʀᴇꜱᴍɪ ᴛᴇʟᴇɢʀᴀᴍ. ᴋɪʀɪᴍ ᴋᴏᴅᴇ ᴏᴛᴘ ᴋᴇ sɪɴɪ sᴇᴛᴇʟᴀʜ ᴍᴇᴍʙᴀᴄᴀ ꜰᴏʀᴍᴀᴛ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ.</b>\n"
                "\n✮ ᴊɪᴋᴀ ᴋᴏᴅᴇ ᴏᴛᴘ ᴀᴅᴀʟᴀʜ <ᴄᴏᴅᴇ>12345</ᴄᴏᴅᴇ> ᴛᴏʟᴏɴɢ <b>[ ᴛᴀᴍʙᴀʜᴋᴀɴ sᴘᴀsɪ ]</b> ᴋɪʀɪᴍᴋᴀɴ sᴇᴘᴇʀᴛɪ ɪɴɪ <code>1 2 3 4 5</code>\n"
                "\n<b>✮ ɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b>"
            ),
            timeout=300,
        )
    except asyncio.TimeoutError:
        return await bot.send_message(user_id, "<blockquote>✮ ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪꜱ!\n✮ ɢᴜɴᴀᴋᴀɴ /ꜱᴛᴀʀᴛ ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>")
    if await is_cancel(callback_query, otp.text):
        return
    otp_code = otp.text
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except PhoneCodeInvalid as PCI:
        return await bot.send_message(user_id, PCI)
    except PhoneCodeExpired as PCE:
        return await bot.send_message(user_id, PCE)
    except BadRequest as error:
        return await bot.send_message(user_id, f"ERROR: {error}")
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                user_id,
                "✮ ᴀᴋᴜɴ ᴀɴᴅᴀ ᴛᴇʟᴀʜ ᴍᴇɴɢᴀᴋᴛɪꜰᴋᴀɴ ᴠᴇʀɪꜰɪᴋᴀsɪ ᴅᴜᴀ ʟᴀɴɢᴋᴀʜ. sɪʟᴀʜᴋᴀɴ ᴋɪʀɪᴍᴋᴀɴ ᴘᴀssᴡᴏʀᴅɴʏᴀ.\n\n✮ ɢᴜɴᴀᴋᴀɴ /cancel ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴀᴛᴀʟᴋᴀɴ ᴘʀᴏsᴇs ᴍᴇᴍʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ</b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await bot.send_message(user_id, "<blockquote>✮ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪꜱ!\n✮ ɢᴜɴᴀᴋᴀɴ /ꜱᴛᴀʀᴛ ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>")
        if await is_cancel(callback_query, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
        except Exception as error:
            return await bot.send_message(user_id, f"ERROR: {error}")
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False
    bot_msg = await bot.send_message(
        user_id,
        "sᴇᴅᴀɴɢ ᴍᴇᴍᴘʀᴏsᴇs....\n\n✮ sɪʟᴀʜᴋᴀɴ ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ",
        disable_web_page_preview=True,
    )
    await new_client.start()
    if not user_id == new_client.me.id:
        ubot._ubot.remove(new_client)
        return await bot_msg.edit(
            "<b>✮ ʜᴀʀᴀᴘ ɢᴜɴᴀᴋᴀɴ ɴᴏᴍᴇʀ ᴛᴇʟᴇɢʀᴀᴍ ᴀɴᴅᴀ ᴅɪ ᴀᴋᴜɴ ᴀɴᴅᴀ sᴀᴀᴛ ɪɴɪ ᴅᴀɴ ʙᴜᴋᴀɴ ɴᴏᴍᴇʀ ᴛᴇʟᴇɢʀᴀᴍ ᴅᴀʀɪ ᴀᴋᴜɴ ʟᴀɪɴ</>"
        )
    await add_ubot(
        user_id=int(new_client.me.id),
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
    )
#    await remove_from_vars(client.me.id, "PREM_USERS", user_id)
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"ZallUbot.modules.{mod}"))
    SH = await ubot.get_prefix(new_client.me.id)
    await edit_rich_message(
        bot_msg,
        "🛡️ ZALLUBOT",
        [
            ("STATUS", "✅ Berhasil diaktifkan"),
            (
                "NAMA",
                f"{new_client.me.first_name} {new_client.me.last_name or ''}".strip(),
            ),
            ("ID", str(new_client.me.id)),
            ("PREFIX", " ".join(SH)),
            (
                "INFO",
                "Harap hubungi admin untuk info terbaru — jika bot tidak respon, ketik /restart",
            ),
        ],
        buttons=[
            [btn("ᴋᴇᴍʙᴀʟɪ", callback_data=f"home {user_id}", style="primary")],
        ],
    )
    await bash("rm -rf *session*")
    await install_my_peer(new_client)
    try:
        await new_client.join_chat("q1ngzs")
        await new_client.join_chat("q1ngzs")
        await new_client.join_chat("q1ngzs")
    except UserAlreadyParticipant:
        pass

    return await send_rich(
        bot,
        LOGS_MAKER_UBOT,
        "🛡️ ZALLUBOT — LOG",
        [
            ("STATUS", "⌬ Userbot diaktifkan"),
            (
                "AKUN",
                f"{new_client.me.first_name} {new_client.me.last_name or ''}".strip(),
            ),
            ("ID", str(new_client.me.id)),
        ],
        buttons=[
            [
                btn(
                    "⦪ ᴄᴇᴋ ᴍᴀsᴀ ᴀᴋᴛɪғ ⦫",
                    callback_data=f"cek_masa_aktif {new_client.me.id}",
                    style="primary",
                )
            ],
        ],
    )

async def is_cancel(callback_query, text):
    if text.startswith("/cancel"):
        await bot.send_message(
            callback_query.from_user.id, "<blockquote>✮ ᴘᴇᴍʙᴀᴛᴀʟᴀɴ ᴏᴛᴏᴍᴀᴛɪꜱ!\n✮ɢᴜɴᴀᴋᴀɴ /ꜱᴛᴀʀᴛ ᴜɴᴛᴜᴋ ᴍᴇᴍᴜʟᴀɪ ᴜʟᴀɴɢ</blockquote>"
        )
        return True
    return False


@PY.BOT("control")
async def _(client, message):
    await reply_rich(
        message,
        "🛡️ ZALLUBOT",
        [("INFO", "Anda akan melakukan restart?! Jika iya, pencet tombol di bawah ini")],
        buttons=[
            [btn("ʀᴇꜱᴛᴀʀᴛ", callback_data="ress_ubot", style="danger")],
        ],
    )

@PY.CALLBACK("ress_ubot")
async def _(client, callback_query):
    if callback_query.from_user.id not in ubot._get_my_id:
        return await callback_query.answer(
            f"you don't have acces",
            True,
        )
    for X in ubot._ubot:
        if callback_query.from_user.id == X.me.id:
            for _ubot_ in await get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        ubot._get_my_id.remove(X.me.id)
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(
                                importlib.import_module(f"ZallUbot.modules.{mod}")
                            )
                        return await edit_rich_query(
                            callback_query,
                            "🛡️ ZALLUBOT",
                            [
                                ("STATUS", "✅ Restart berhasil dilakukan"),
                                (
                                    "NAMA",
                                    f"{UB.me.first_name} {UB.me.last_name or ''}".strip(),
                                ),
                                ("ID", str(UB.me.id)),
                            ],
                        )
                    except Exception as error:
                        return await callback_query.edit_message_text(f"{error}")

@PY.BOT("restart")
async def _(client, message):
    msg = await message.reply("<b>✮ ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ</b>")
    if message.from_user.id not in ubot._get_my_id:
        return await msg.edit(
            f"you don't have acces",
            True,
        )
    for X in ubot._ubot:
        if message.from_user.id == X.me.id:
            for _ubot_ in await get_userbots():
                if X.me.id == int(_ubot_["name"]):
                    try:
                        ubot._ubot.remove(X)
                        ubot._get_my_id.remove(X.me.id)
                        UB = Ubot(**_ubot_)
                        await UB.start()
                        for mod in loadModule():
                            importlib.reload(
                                importlib.import_module(f"ZallUbot.modules.{mod}")
                            )
                        return await edit_rich_message(
                            msg,
                            "🛡️ ZALLUBOT",
                            [
                                ("STATUS", "✅ Restart berhasil dilakukan"),
                                (
                                    "NAMA",
                                    f"{UB.me.first_name} {UB.me.last_name or ''}".strip(),
                                ),
                                ("ID", str(UB.me.id)),
                            ],
                        )
                    except Exception as error:
                        return await msg.edit(f"{error}")

def _ubot_rows(count):
    x = ubot._ubot[count]
    return [
        ("USERBOT KE", f"{count + 1}/{len(ubot._ubot)}"),
        ("AKUN", f"{x.me.first_name} {x.me.last_name or ''}".strip()),
        ("USER ID", str(x.me.id)),
    ]


def _ubot_buttons(count):
    x = ubot._ubot[count]
    return [
        [
            btn(
                "⦪ ʜᴀᴘᴜs ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀsᴇ ⦫",
                callback_data=f"del_ubot {x.me.id}",
                style="danger",
            )
        ],
        [
            btn(
                "⦪ ᴄᴇᴋ ᴍᴀsᴀ ᴀᴋᴛɪғ ⦫",
                callback_data=f"cek_masa_aktif {x.me.id}",
                style="primary",
            )
        ],
        [
            btn("⟢", callback_data=f"p_ub {count}", style="primary"),
            btn("⟣", callback_data=f"n_ub {count}", style="primary"),
        ],
    ]


@PY.CALLBACK("cek_ubot")
@PY.BOT("getubot")
@PY.ADMIN
async def _(client, callback_query):
    await send_rich(
        bot,
        callback_query.from_user.id,
        "🛡️ ZALLUBOT — LIST USERBOT",
        _ubot_rows(0),
        buttons=_ubot_buttons(0),
    )

@PY.CALLBACK("cek_masa_aktif")
async def _(client, callback_query):
    user_id = int(callback_query.data.split()[1])
    expired = await get_expired_date(user_id)
    try:
        xxxx = (expired - datetime.now()).days
        return await callback_query.answer(f"✮ ᴛɪɴɢɢᴀʟ {xxxx} ʜᴀʀɪ ʟᴀɢɪ", True)
    except:
        return await callback_query.answer("✮ sᴜᴅᴀʜ ᴛɪᴅᴀᴋ ᴀᴋᴛɪғ", True)

@PY.CALLBACK("del_ubot")
async def _(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in await get_list_from_vars(client.me.id, "ADMIN_USERS"):
        return await callback_query.answer(
            f"❌ ᴛᴏᴍʙᴏʟ ɪɴɪ ʙᴜᴋᴀɴ ᴜɴᴛᴜᴋ ᴍᴜ {callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}",
            True,
        )
    try:
        show = await bot.get_users(callback_query.data.split()[1])
        get_id = show.id
        get_mention = f"{get_id}"
    except Exception:
        get_id = int(callback_query.data.split()[1])
        get_mention = f"{get_id}"
    for X in ubot._ubot:
        if get_id == X.me.id:
            await X.unblock_user(bot.me.username)
            await remove_ubot(X.me.id)
            ubot._get_my_id.remove(X.me.id)
            ubot._ubot.remove(X)
            await X.log_out()
            await callback_query.answer(
                f"✮ {get_mention} ʙᴇʀʜᴀsɪʟ ᴅɪʜᴀᴘᴜs ᴅᴀʀɪ ᴅᴀᴛᴀʙᴀsᴇ", True
            )
            await edit_rich_query(
                callback_query,
                "🛡️ ZALLUBOT — LIST USERBOT",
                _ubot_rows(0),
                buttons=_ubot_buttons(0),
            )
            await send_rich(
                bot,
                X.me.id,
                "🛡️ ZALLUBOT",
                [
                    ("PEMBERITAHUAN", "Masa aktif userbot Anda telah habis"),
                    ("AKUN", f"{X.me.first_name} {X.me.last_name or ''}".strip()),
                    ("ID", str(X.me.id)),
                ],
                buttons=[
                    [btn("beli userbot", callback_data="bahan", style="success")],
                ],
            )

    
@PY.CALLBACK("^(p_ub|n_ub)")
async def _(client, callback_query):
    query = callback_query.data.split()
    count = int(query[1])
    if query[0] == "n_ub":
        if count == len(ubot._ubot) - 1:
            count = 0
        else:
            count += 1
    elif query[0] == "p_ub":
        if count == 0:
            count = len(ubot._ubot) - 1
        else:
            count -= 1
    await edit_rich_query(
        callback_query,
        "🛡️ ZALLUBOT — LIST USERBOT",
        _ubot_rows(count),
        buttons=_ubot_buttons(count),
    )
