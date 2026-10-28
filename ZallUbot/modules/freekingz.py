import random
import re
import os
import platform
import subprocess
import sys
import traceback
from datetime import datetime
from io import BytesIO, StringIO
from ZallUbot.config import OWNER_ID
import psutil
from ZallUbot import *
from datetime import datetime
from time import time

from pyrogram.raw.functions import Ping
from pyrogram.types import *

from ZallUbot import *

@PY.BOT("freedewa")
@PY.PRIVATE
async def _(client, message):
    buttons = BTN.PROMODEK(message)
    sh = await message.reply("""<u><b>𝗙𝗜𝗧𝗨𝗥 𝗙𝗥𝗘𝗘 𝗗𝗘𝗪𝗔 𝗨𝗦𝗘𝗥𝗕𝗢𝗧!</b></u>
<blockquote><b>/ai -  ᴘᴇʀᴛᴀɴʏᴀᴀɴ ᴍᴜ</b>
<b>/joko - ᴊᴏᴋᴏ ᴀɪ ʏᴀɪᴛᴜ ᴀɪ ʏᴀɴɢ ʙᴇʀʙᴀʜᴀsᴀ ᴊᴀᴡᴀ</b>
<b>/brat - ᴍᴀsᴜᴋᴋᴀɴ ᴛᴇxᴛ ᴜɴᴛᴜᴋ ᴅɪ ᴊᴀᴅɪᴋᴀɴ ғᴏᴛᴏ</b>
<b>/adzan - ᴍᴀsᴜᴋᴋᴀɴ ᴋᴏᴛᴀ ᴜɴᴛᴜᴋ ᴄᴇᴋ ᴊᴀᴅᴡᴀʟ ᴀᴅᴢᴀɴ</b>
<b>/tourl - ʀᴇᴘʟʏ ғᴏᴛᴏ ʏᴀɴɢ ɪɴɢɪɴ ᴅɪ ᴊᴀᴅɪᴋᴀɴ ʟɪɴᴋ</b>
<b>/gempa - ᴜɴᴛᴜᴋ ᴍᴇʟɪʜᴀᴛ ɪɴғᴏʀᴍᴀsɪ ɢᴇᴍᴘᴀ ᴛᴇʀᴋɪɴɪ ᴅɪ ɪɴᴅᴏɴᴇsɪᴀ</b>
<b>/tiktok - ʙᴇʀɪᴋᴀɴ ʟɪɴᴋ ᴠᴛ/ʟɪɴᴋ ғɪᴅɪᴏ ᴛɪᴋᴛᴏᴋ ᴜɴᴛᴜᴋ ᴅɪ ᴅᴏᴡɴʟᴏᴀᴅ</b></blockquote>

<blockquote><b>ᴏᴡɴᴇʀ ᴜsᴇʀʙᴏᴛ ᴅɪ ʙᴀᴡᴀʜ sɪɴɪʜ</b>
<b>ᴏᴡɴᴇʀ ᴜsᴇʀʙᴏᴛ: <a href=https://t.me/GanzVil21>ᴏᴡɴᴇʀ ᴅᴇᴡᴀ</a></b></blockquote>""", reply_markup=InlineKeyboardMarkup(buttons))
