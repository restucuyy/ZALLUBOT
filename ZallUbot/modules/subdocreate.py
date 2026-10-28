import os

import requests
import json
from pyrogram import *
from pyrogram import Client, filters
from ZallUbot import PY

__MODULE__ = "Subdomain Creator"
__HELP__ = """
<blockquote><b>Bantuan Untuk Subdomain Creator</b>

Perintah:
<code>{0}subdocreate [domain] [subdomain] [IP]</code> → Menambahkan subdomain ke domain yang tersedia di Cloudflare.
<code>{0}listdomain </code> → Untuk melihat list domain.

🔍 Contoh:
<code>{0}subdocreate example.com test 192.168.1.1</code>

💡 Gunakan <code>{0}domainlist</code> untuk melihat daftar domain yang tersedia.</blockquote></b>
"""

# Konfigurasi Cloudflare (Tambahkan daftar domain dengan Zone ID)
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN", "")  # isi di .env
DOMAIN_LIST = {
    # "domainkamu.com": "ZONE_ID_DARI_CLOUDFLARE",
}

# Fungsi untuk menambahkan subdomain ke Cloudflare
def create_subdomain(zone_id, subdomain, target_ip):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "type": "A",  # Bisa diubah ke "CNAME" jika ingin menggunakan CNAME
        "name": subdomain,
        "content": target_ip,
        "ttl": 1,
        "proxied": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

@PY.UBOT("subdocreate")
@PY.TOP_CMD
async def subdomain_create(client, message):
    args = message.text.split(maxsplit=3)
    if len(args) < 4:
        await message.reply_text("❌ Silakan masukkan format yang benar: `.subdocreate [domain] [subdomain] [IP]`")
        return

    domain = args[1].strip()
    subdomain = args[2].strip()
    target_ip = args[3].strip()

    if domain not in DOMAIN_LIST:
        await message.reply_text(f"❌ Domain `{domain}` tidak ditemukan dalam daftar. Gunakan `.domainlist` untuk melihat daftar domain yang tersedia.")
        return

    zone_id = DOMAIN_LIST[domain]
    full_subdomain = f"{subdomain}.{domain}"

    await message.reply_text(f"🔍 **Menambahkan subdomain:** `{full_subdomain}` ➝ `{target_ip}`")

    result = create_subdomain(zone_id, full_subdomain, target_ip)

    if result.get("success"):
        await message.reply_text(f"✅ **Subdomain Berhasil Ditambahkan!**\n🌐 `{full_subdomain} → {target_ip}`")
    else:
        error_msg = result.get("errors", [{"message": "Unknown Error"}])[0]["message"]
        await message.reply_text(f"❌ **Gagal Menambahkan Subdomain**\n⚠️ Error: `{error_msg}`")

@PY.UBOT("domainlist")
@PY.TOP_CMD
async def list_domains(client, message):
    domain_list_text = "📜 **Daftar Domain yang Tersedia:**\n"
    for domain in DOMAIN_LIST.keys():
        domain_list_text += f"✅ `{domain}`\n"
    
    await message.reply_text(domain_list_text)