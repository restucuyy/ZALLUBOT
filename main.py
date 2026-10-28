# ZALLUBOT - file utama untuk Panel Pterodactyl (egg Python)
# =====================================================================
# Di panel Pterodactyl, isi "App Py File" / PY_FILE dengan:  main.py
# File ini menjalankan ZallUbot PERSIS seperti perintah
# `python3 -m ZallUbot` - tidak ada logika bot yang diubah sama sekali.
#
# Dua persiapan teknis ditambahkan di sini (bukan di file bot):
# 1) Event loop untuk Python 3.12 + uvloop 0.23: tanpa loop yang disiapkan
#    sebelum ZallUbot dibaca, pyrogram gagal import dengan
#    "RuntimeError: There is no current event loop in thread 'MainThread'"
#    karena ZallUbot/__init__.py memanggil uvloop.install() lalu pyrogram
#    langsung meminta event loop. Launcher memasang policy + loop lebih
#    dulu, lalu membuat uvloop.install() kedua dari bot menjadi no-op.
#    Terverifikasi lolos import pyrogram (Python 3.12.3, uvloop 0.23.0).
# 2) PATH untuk modul encode.py: modul itu memeriksa `shutil.which(
#    "uglifyjs")` saat dimuat. Node.js + UglifyJS resmi dipasang di dalam
#    folder server (folder `node/`), jadi launcher menambahkan
#    /home/container/node/bin ke PATH proses bot.
# =====================================================================
import asyncio
import os

os.environ["PATH"] = "/home/container/node/bin:" + os.environ.get("PATH", "")

import uvloop

uvloop.install()
asyncio.set_event_loop(uvloop.new_event_loop())
uvloop.install = lambda: None

import runpy

if __name__ == "__main__":
    runpy.run_module("ZallUbot", run_name="__main__")
