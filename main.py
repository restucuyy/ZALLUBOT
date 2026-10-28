# ZALLUBOT - file utama untuk Panel Pterodactyl (egg Python)
# =====================================================================
# Di panel Pterodactyl, isi "App Py File" / PY_FILE dengan:  main.py
# File ini hanya menjalankan ZallUbot PERSIS seperti perintah
# `python3 -m ZallUbot` - tidak ada logika yang diubah sama sekali.
# =====================================================================
import runpy

if __name__ == "__main__":
    runpy.run_module("ZallUbot", run_name="__main__")
