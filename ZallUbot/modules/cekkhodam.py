import asyncio
import random

from ZallUbot import *

__MODULE__ = "ᴄᴇᴋᴋʜᴏᴅᴀᴍ"
__HELP__ = """**「 BANTUAN UNTUK MODULE CEK KHODAM 」**

𖠇➛ **ᴘᴇʀɪɴᴛᴀʜ: .cekkhodam**
𖠇➛ **ᴘᴇɴᴊᴇʟᴀsᴀɴ: ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ᴋʜᴏᴅᴀᴍ ɴᴀᴍᴀ ᴏʀᴀɴɢ**"""


@PY.UBOT("cekkhodam")
@PY.TOP_CMD
async def cekkhodam(client, message):
    try:
        nama = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
        if not nama:
            await message.edit("ɴᴀᴍᴀɴʏᴀ ᴍᴀɴᴀ ᴀɴᴊᴇɴɢ🤓")
            return

        def pick_random(options):
            return random.choice(options)

        hasil = f"""
 <b>𖤐 ʜᴀsɪʟ ᴄᴇᴋ ᴋʜᴏᴅᴀᴍ:</b>
╭───────────────────────
├ •ɴᴀᴍᴀ : {nama}
├ •ᴋʜᴏᴅᴀᴍɴʏᴀ : {pick_random(['lonte gurun', 'dugong', 'macan yatim', 'buaya darat', 'kanjut terbang', 'kuda kayang', 'janda salto', 'lonte alas', 'jembut singa', 'gajah terbang', 'kuda cacat', 'jembut pink', 'sabun bolong'])}
├ •ɴɢᴇʀɪ ʙᴇᴛ ᴊɪʀ ᴋʜᴏᴅᴀᴍɴʏᴀ
╰────────────────────────
  **ɴᴇxᴛ ᴄᴇᴋ ᴋʜᴏᴅᴀᴍɴʏᴀ sɪᴀᴘᴀ ʟᴀɢɪ.**       
      """
        await message.edit(hasil)
    except BaseException:
        pass
