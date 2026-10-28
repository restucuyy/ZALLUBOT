import asyncio
import psutil
from datetime import datetime
from speedtest import Speedtest
from pyrogram import Client, filters
from ZallUbot import *

__MODULE__ = "sᴘᴇᴇᴅ ᴛᴇsᴛ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ sᴘᴇᴇᴅ ᴛᴇsᴛ ⦫</b>

<blockquote><b>⎆ ᴘᴇʀɪɴᴛᴀʜ :
ᚗ <code>{0}speed</code>

⌭ ᴘᴇɴᴊᴇʟᴀsᴀɴ:
ᚗ Untuk melakukan speestest VPS</b></blockquote>
"""

def humanbytes(size):
    power = 2**10
    n = 0
    power_labels = {0: "B", 1: "KB", 2: "MB", 3: "GB", 4: "TB"}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]}"

def get_vps_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    uptime = now - boot_time

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return f"{days} hari, {hours} jam, {minutes} menit"

@PY.UBOT("speed")
async def speedtest_cmd(client, message):
    msg = await message.reply("**__🔄 Sedang melakukan Speedtest...__**")

    try:
        test = Speedtest()
        test.get_best_server()
        
        download_speed = await asyncio.to_thread(test.download)
        upload_speed = await asyncio.to_thread(test.upload)
        test.results.share()

        result = test.results.dict()
        vps_uptime = get_vps_uptime()
        caption = (
            f"""
<blockquote>**Speedtest Result**

🌍 **ISP:** `{result['client']['isp']}`
🏳️ **Country:** `{result['client']['country']}`
⏳ **VPS Uptime:** `{vps_uptime}`

**Server**
🏠 **Name:** `{result['server']['name']}`
🏳️ **Country:** `{result['server']['country']}`
⚡ **Ping:** `{result['ping']}` ms
📥 **Download:** `{humanbytes(result['download'])}/s`
📤 **Upload:** `{humanbytes(result['upload'])}/s`</blockquote>"""
        )

        await msg.delete()
        await client.send_photo(
            message.chat.id,
            result["share"],
            caption=caption,
        )

    except Exception as e:
        await msg.edit(f"**__⚠️ Gagal melakukan Speedtest! Error: {e}__**")
