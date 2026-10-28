# ZALLUBOT - config
# Semua nilai dibaca dari file .env (salin sample.env menjadi .env lalu isi).
# Default rahasia owner lama SUDAH DIHAPUS. Bot tidak akan lagi memakai
# API_HASH / BOT_TOKEN milik orang lain kalau .env belum diisi.
# Database TIDAK lagi memakai MongoDB: semua data disimpan lokal di
# data/zallubot.db (SQLite, dibuat otomatis, tanpa URL / tanpa server).
import os
from dotenv import load_dotenv

load_dotenv(".env")

MAX_BOT = int(os.getenv("MAX_BOT", "100"))

# ID Telegram developer/owner ZALLUBOT (pisahkan dengan spasi bila lebih dari satu)
DEVS = list(map(int, os.getenv("DEVS", "").split()))

API_ID = int(os.getenv("API_ID", "0"))

API_HASH = os.getenv("API_HASH", "")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

OWNER_ID = int(os.getenv("OWNER_ID", "0"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "").split()))

RMBG_API = os.getenv("RMBG_API", "")

# File database lokal (opsional, default data/zallubot.db)
DB_PATH = os.getenv("DB_PATH", "data/zallubot.db")

# KiPay.id - pengganti QRIS OrderKuota / OkeConnect (untuk modul qris)
# API key dari project PRODUCTION di console.kipay.id -> transaksi asli
KIPAY_API_KEY = os.getenv("KIPAY_API_KEY", "")
KIPAY_MODE = os.getenv("KIPAY_MODE", "production").lower()
KIPAY_BASE = "https://api.kipay.id"

LOGS_MAKER_UBOT = int(os.getenv("LOGS_MAKER_UBOT", "0"))

# Rich Message (Bot API 10.1) untuk layar BOT pembuat userbot: "on" / "off"
# Default "on". Hanya berlaku untuk pesan BOT; pesan akun userbot tetap
# memakai tampilan klasik. Lihat ZallUbot/core/rich.py dan VERSI_RICH.md.
RICH_MESSAGES = os.getenv("RICH_MESSAGES", "on")
