# ZALLUBOT - Rich Message UI layer (Bot API 10.1)
# =====================================================================
# Lapisan tampilan "Rich Message" khusus untuk BOT pembuat userbot.
#
# Rich Message adalah fitur Bot API (HTTP), jadi hanya bisa dipakai oleh
# pesan yang dikirim BOT (BOT_TOKEN). Pesan dari akun USERBOT (Pyrogram /
# MTProto) TIDAK bisa memakai rich message dan tetap tampil klasik.
#
# Cara kerja helper di file ini:
#   1. Coba kirim / edit lewat Bot API (sendRichMessage / editMessageText
#      dengan parameter rich_message).
#   2. Kalau gagal (API error, token kosong, RICH_MESSAGES=off, pesan
#      media, dll) -> fallback otomatis ke tampilan klasik Pyrogram
#      (reply_text / edit_text) dengan isi tabel yang sama dalam bentuk
#      teks biasa "label: value" dan keyboard Pyrogram (tanpa style).
#
# Semua callback_data dan alur handler TIDAK berubah; yang berubah hanya
# lapisan presentasi. Matikan fitur ini lewat .env: RICH_MESSAGES=off
# =====================================================================
import html
import os

try:
    from ZallUbot.config import BOT_TOKEN as _CFG_BOT_TOKEN
    from ZallUbot.config import OWNER_ID as _CFG_OWNER_ID
    from ZallUbot.config import RICH_MESSAGES as _CFG_RICH_MESSAGES
except Exception:  # fallback bila config belum bisa diimpor (mis. unit test)
    _CFG_BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    try:
        _CFG_OWNER_ID = int(os.getenv("OWNER_ID", "0") or 0)
    except Exception:
        _CFG_OWNER_ID = 0
    _CFG_RICH_MESSAGES = os.getenv("RICH_MESSAGES", "on")

_BOT_API_BASE = "https://api.telegram.org"
DEFAULT_FOOTER = "© ZALLUBOT"


def _bot_token():
    return _CFG_BOT_TOKEN or os.getenv("BOT_TOKEN", "")


def _rich_enabled():
    val = os.getenv("RICH_MESSAGES", None)
    if val is None:
        val = _CFG_RICH_MESSAGES
    return str(val).strip().lower() in ("on", "1", "true", "yes")


def _esc(value):
    return html.escape(str(value), quote=True)


# ---------------------------------------------------------------------
# Pembangun HTML Rich Message
# ---------------------------------------------------------------------
def rich_table(title, rows, footer=None):
    """Bangun HTML Rich Message: judul + tabel 2 kolom INFO | KETERANGAN.

    rows: list berisi tuple (label, value). Semua nilai di-escape HTML.
    footer: teks kecil di bawah tabel (opsional).
    """
    parts = [f"<h3>{_esc(title)}</h3>", "<table bordered striped>"]
    parts.append("<tr><th>INFO</th><th>KETERANGAN</th></tr>")
    for label, value in rows:
        parts.append(f"<tr><td>{_esc(label)}</td><td>{_esc(value)}</td></tr>")
    parts.append("</table>")
    if footer:
        parts.append(f"<p>{_esc(footer)}</p>")
    return "\n".join(parts)


def _plain_table(title, rows, footer=None):
    """Render teks biasa (fallback klasik) dari tabel yang sama."""
    lines = [f"<b>{_esc(title)}</b>", ""]
    for label, value in rows:
        lines.append(f"<b>{_esc(label)}:</b> {_esc(value)}")
    if footer:
        lines += ["", f"<i>{_esc(footer)}</i>"]
    return "\n".join(lines)


# ---------------------------------------------------------------------
# Pembangun tombol (Bot API reply_markup, mendukung style Bot API 9.4)
# ---------------------------------------------------------------------
def btn(text, callback_data=None, url=None, style=None):
    """Satu tombol inline dalam bentuk dict Bot API.

    style: "primary" | "success" | "danger" (Bot API 9.4, opsional).
    """
    button = {"text": text}
    if callback_data is not None:
        button["callback_data"] = callback_data
    if url is not None:
        button["url"] = url
    if style:
        button["style"] = style
    return button


def kb(*rows):
    """Susun reply_markup Bot API dari baris-baris tombol btn()."""
    return {"inline_keyboard": [list(row) for row in rows]}


def _pyro_markup(buttons):
    """Konversi tombol format btn() menjadi InlineKeyboardMarkup Pyrogram
    (untuk fallback klasik; field style diabaikan)."""
    if not buttons:
        return None
    try:
        from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    except Exception:
        return None
    keyboard = []
    for row in buttons:
        keyboard.append(
            [
                InlineKeyboardButton(
                    b.get("text", ""),
                    callback_data=b.get("callback_data"),
                    url=b.get("url"),
                )
                for b in row
            ]
        )
    return InlineKeyboardMarkup(keyboard)


# ---------------------------------------------------------------------
# Pemanggil Bot API (HTTP) memakai BOT_TOKEN + aiohttp
# ---------------------------------------------------------------------
async def _post_bot_api(method, payload):
    """POST ke Bot API. Return dict 'result' bila ok, None bila gagal."""
    token = _bot_token()
    if not token:
        return None
    url = f"{_BOT_API_BASE}/bot{token}/{method}"
    try:
        session = None
        try:
            from ZallUbot import aiosession as _shared_session

            if _shared_session is not None and not getattr(
                _shared_session, "closed", False
            ):
                session = _shared_session
        except Exception:
            session = None
        if session is not None:
            async with session.post(url, json=payload) as resp:
                data = await resp.json(content_type=None)
        else:
            from aiohttp import ClientSession

            async with ClientSession() as own_session:
                async with own_session.post(url, json=payload) as resp:
                    data = await resp.json(content_type=None)
        if isinstance(data, dict) and data.get("ok"):
            return data.get("result", data)
        return None
    except Exception:
        return None


async def rich_send(chat_id, html_text, markup=None):
    """Kirim Rich Message via Bot API sendRichMessage.

    Return result dict bila sukses, None bila gagal.
    """
    payload = {"chat_id": chat_id, "rich_message": {"html": html_text}}
    if markup:
        payload["reply_markup"] = markup
    return await _post_bot_api("sendRichMessage", payload)


async def rich_edit(chat_id, message_id, html_text, markup=None):
    """Edit pesan menjadi Rich Message via Bot API editMessageText.

    Return result dict bila sukses, None bila gagal.
    """
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "rich_message": {"html": html_text},
    }
    if markup:
        payload["reply_markup"] = markup
    return await _post_bot_api("editMessageText", payload)


# ---------------------------------------------------------------------
# Helper tingkat tinggi untuk handler Pyrogram (rich + fallback klasik)
# ---------------------------------------------------------------------
async def reply_rich(message, title, rows, buttons=None, footer=DEFAULT_FOOTER):
    """Balas `message` dengan tabel rich. Fallback: reply_text klasik."""
    if _rich_enabled():
        result = await rich_send(
            message.chat.id,
            rich_table(title, rows, footer),
            kb(*buttons) if buttons else None,
        )
        if result is not None:
            return result
    return await message.reply_text(
        _plain_table(title, rows, footer),
        reply_markup=_pyro_markup(buttons),
        disable_web_page_preview=True,
    )


async def send_rich(client, chat_id, title, rows, buttons=None, footer=DEFAULT_FOOTER):
    """Kirim tabel rich ke chat_id lewat bot client. Fallback: send_message."""
    if _rich_enabled():
        result = await rich_send(
            chat_id,
            rich_table(title, rows, footer),
            kb(*buttons) if buttons else None,
        )
        if result is not None:
            return result
    return await client.send_message(
        chat_id,
        _plain_table(title, rows, footer),
        reply_markup=_pyro_markup(buttons),
        disable_web_page_preview=True,
    )


async def edit_rich_message(message, title, rows, buttons=None, footer=DEFAULT_FOOTER):
    """Edit objek Message menjadi tabel rich. Fallback: edit_text klasik."""
    if _rich_enabled():
        result = await rich_edit(
            message.chat.id,
            message.id,
            rich_table(title, rows, footer),
            kb(*buttons) if buttons else None,
        )
        if result is not None:
            return result
    return await message.edit_text(
        _plain_table(title, rows, footer),
        reply_markup=_pyro_markup(buttons),
        disable_web_page_preview=True,
    )


async def edit_rich_query(query, title, rows, buttons=None, footer=DEFAULT_FOOTER):
    """Edit pesan dari CallbackQuery menjadi tabel rich.

    Urutan percobaan:
      1. Bot API editMessageText (rich) pada pesan yang sama.
      2. Kirim Rich Message baru lalu hapus pesan lama (diperlukan bila
         pesan lama adalah pesan media/foto dari /start, yang tidak bisa
         diedit teksnya lewat Bot API).
      3. Fallback klasik: query.message.edit_text (Pyrogram/MTProto).
    """
    message = query.message
    if _rich_enabled():
        html_text = rich_table(title, rows, footer)
        markup = kb(*buttons) if buttons else None
        result = await rich_edit(message.chat.id, message.id, html_text, markup)
        if result is not None:
            return result
        sent = await rich_send(message.chat.id, html_text, markup)
        if sent is not None:
            try:
                await message.delete()
            except Exception:
                pass
            return sent
    return await message.edit_text(
        _plain_table(title, rows, footer),
        reply_markup=_pyro_markup(buttons),
        disable_web_page_preview=True,
    )


# ---------------------------------------------------------------------
# Kit layar khusus ZALLUBOT (dipakai handler bot pembuat userbot)
# ---------------------------------------------------------------------
def home_table(first_name, last_name, bot_username, total_ubot):
    """(title, rows, footer) untuk layar utama / home bot."""
    name = f"{first_name} {last_name or ''}".strip()
    rows = [
        ("👋 HALO", name),
        ("BOT", f"@{bot_username}" if bot_username else "ZALLUBOT"),
        ("FUNGSI", "Membuat userbot dengan mudah"),
        ("STATUS", "✅ ONLINE"),
        ("TOTAL USERBOT", str(total_ubot)),
        ("OWNER", "ZALLUBOT"),
    ]
    return (
        "🛡️ ZALLUBOT",
        rows,
        "© ZALLUBOT — Klik tombol di bawah untuk membuat userbot",
    )


def start_buttons(user_id):
    """Tombol menu utama (mirror BTN.START) dalam format btn() + style."""
    if int(user_id) != int(_CFG_OWNER_ID or 0):
        return [
            [btn("⦪ ʙᴇʟɪ ᴜꜱᴇʀʙᴏᴛ ⦫", callback_data="bahan", style="success")],
            [
                btn("⦪ ɢʀᴏᴜᴘ ᴘᴜʙʟɪᴄ ⳼", url="t.me/publikibnu", style="primary"),
                btn("⦪ ᴄʜᴀɴɴᴇʟ ⦫", url="t.me/MizukiOgawaRR", style="primary"),
            ],
            [
                btn("⦪ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ⳼", callback_data="buat_ubot", style="primary"),
                btn("⦪ ʜᴇʟᴘ ᴍᴇɴᴜ ⦫", callback_data="help_back", style="primary"),
            ],
            [btn("⦪ sᴜᴘᴘᴏʀᴛ ⦫", callback_data="support", style="primary")],
        ]
    return [
        [btn("⦪ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ ⦫", callback_data="bahan", style="success")],
        [
            btn("⦪ ɢɪᴛᴘᴜʟʟ ⦫", callback_data="cb_gitpull", style="primary"),
            btn("⦪ ʀᴇsᴛᴀʀᴛ ⦫", callback_data="cb_restart", style="danger"),
        ],
        [btn("⦪ ʟɪsᴛ ᴜsᴇʀʙᴏᴛ ⦫", callback_data="cek_ubot", style="primary")],
    ]


def payment_table(harga, total, bulan):
    """(title, rows, footer) untuk layar pembayaran (mirror MSG.TEXT_PAYMENT)."""
    rows = [
        ("HARGA PERBULAN", f"Rp{harga}.000"),
        ("METODE PEMBAYARAN", "QRIS All Payment"),
        ("TOTAL HARGA", f"Rp{total}.000"),
        ("TOTAL BULAN", f"{bulan} bulan"),
        ("OWNER BOT", "ZALLUBOT"),
        ("INFO", "Klik tombol Konfirmasi untuk kirim bukti pembayaran Anda"),
    ]
    return ("💳 ZALLUBOT — PEMBAYARAN", rows, DEFAULT_FOOTER)


def payment_buttons(bulan, user_id):
    """Tombol +/- bulan + konfirmasi + batal (mirror BTN.PLUS_MINUS)."""
    return [
        [
            btn("-1", callback_data=f"kurang {bulan}"),
            btn("+1", callback_data=f"tambah {bulan}"),
        ],
        [btn("⦪ ᴋᴏɴꜰɪʀᴍᴀsɪ ⦫", callback_data="confirm", style="success")],
        [btn("⦪ ʙᴀᴛᴀʟᴋᴀɴ ⦫", callback_data=f"home {user_id}", style="danger")],
    ]
