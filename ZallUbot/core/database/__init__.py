# ZALLUBOT - Database LOKAL (tanpa MongoDB)
# =====================================================================
# Dulu file ini membuat koneksi MongoDB Atlas (motor / AsyncIOMotorClient).
# Sekarang diganti total menjadi SQLite lokal (modul bawaan Python
# `sqlite3`, TANPA server, TANPA URL, TANPA dependensi tambahan) supaya
# bisa jalan di Panel Pterodactyl.
#
# PENTING: API-nya dibuat PERSIS meniru API motor yang dipakai modul lain:
#   mongo_client["nama_db"]["nama_koleksi"].find_one({...})
#   mongo_client["nama_db"].nama_koleksi.update_one(filter, {"$set": {...}}, upsert=True)
#   mongodb.varsX / mongodb.ubot / collection.find({...})  (async for)
#   $set / $unset dengan kunci bertitik ("vars.NAMA"), $exists, dll.
# Jadi TIDAK ADA file database lain yang diubah: variabel.py, userbot.py,
# pref.py, expired.py, antigcast.py dan semua modul tetap sama persis,
# hanya tempat penyimpanannya yang sekarang file lokal:
#
#   data/zallubot.db   (dibuat otomatis, bisa diatur lewat env DB_PATH)
#
# Backup / pindah panel = cukup salin file data/zallubot.db itu.
# =====================================================================
import base64
import copy
import json
import os
import sqlite3
import threading
from datetime import date, datetime

_DB_PATH = os.getenv("DB_PATH", os.path.join("data", "zallubot.db"))

_lock = threading.Lock()
_conn = None


def _connect():
    global _conn
    if _conn is None:
        folder = os.path.dirname(os.path.abspath(_DB_PATH))
        os.makedirs(folder, exist_ok=True)
        _conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
        _conn.execute(
            "CREATE TABLE IF NOT EXISTS documents ("
            " db TEXT NOT NULL, collection TEXT NOT NULL,"
            " doc_key TEXT NOT NULL, data TEXT NOT NULL,"
            " PRIMARY KEY (db, collection, doc_key))"
        )
        _conn.commit()
    return _conn


# ---------- serialisasi nilai (datetime/dict/list/dll. -> JSON aman) ----------
_TAG = "__zallu_type__"


def _encode(value):
    if isinstance(value, datetime):
        return {_TAG: "datetime", "value": value.isoformat()}
    if isinstance(value, date):
        return {_TAG: "date", "value": value.isoformat()}
    if isinstance(value, bytes):
        return {_TAG: "bytes", "value": base64.b64encode(value).decode()}
    if isinstance(value, dict):
        return {str(k): _encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_encode(v) for v in value]
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    return {_TAG: "str", "value": str(value)}


def _decode(value):
    if isinstance(value, dict):
        tag = value.get(_TAG)
        if tag == "datetime":
            return datetime.fromisoformat(value["value"])
        if tag == "date":
            return date.fromisoformat(value["value"])
        if tag == "bytes":
            return base64.b64decode(value["value"])
        if tag == "str":
            return value["value"]
        return {k: _decode(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_decode(v) for v in value]
    return value


# ---------- helper filter / update ala Mongo ----------
def _matches(doc, filt):
    if not filt:
        return True
    for key, cond in filt.items():
        present = isinstance(doc, dict) and key in doc
        val = doc.get(key) if present else None
        if isinstance(cond, dict) and any(str(k).startswith("$") for k in cond):
            for op, operand in cond.items():
                if op == "$exists":
                    if bool(operand) != present:
                        return False
                elif op == "$ne":
                    if present and val == operand:
                        return False
                elif op == "$in":
                    if val not in operand:
                        return False
                elif op == "$nin":
                    if val in operand:
                        return False
                elif op in ("$gt", "$gte", "$lt", "$lte"):
                    if not present:
                        return False
                    try:
                        if op == "$gt" and not val > operand:
                            return False
                        if op == "$gte" and not val >= operand:
                            return False
                        if op == "$lt" and not val < operand:
                            return False
                        if op == "$lte" and not val <= operand:
                            return False
                    except TypeError:
                        return False
                else:
                    return False
        else:
            if not present or val != cond:
                return False
    return True


def _doc_key(doc, filt=None):
    for key in ("_id", "user_id"):
        if isinstance(doc, dict) and doc.get(key) is not None:
            return key + ":" + json.dumps(_encode(doc[key]), sort_keys=True)
    if filt:
        return "filter:" + json.dumps(_encode(filt), sort_keys=True, default=str)
    return "auto:" + str(id(doc))


def _set_dotted(doc, dotted, value):
    parts = str(dotted).split(".")
    cur = doc
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[part] = nxt
        cur = nxt
    cur[parts[-1]] = value


def _unset_dotted(doc, dotted):
    parts = str(dotted).split(".")
    cur = doc
    for part in parts[:-1]:
        cur = cur.get(part)
        if not isinstance(cur, dict):
            return
    cur.pop(parts[-1], None)


class _Result:
    def __init__(self, matched=0, modified=0, deleted=0, upserted_id=None):
        self.matched_count = matched
        self.modified_count = modified
        self.deleted_count = deleted
        self.upserted_id = upserted_id
        self.inserted_id = upserted_id


class _Cursor:
    def __init__(self, docs):
        self._docs = docs
        self._it = None

    def __aiter__(self):
        self._it = iter(self._docs)
        return self

    async def __anext__(self):
        try:
            return next(self._it)
        except StopIteration:
            raise StopAsyncIteration

    async def to_list(self, length=None):
        return list(self._docs if length is None else self._docs[:length])


class LocalCollection:
    def __init__(self, db_name, coll_name):
        object.__setattr__(self, "_db", db_name)
        object.__setattr__(self, "_coll", coll_name)

    # Sub-koleksi: collection["x"] / collection.x (dipakai pref.py & expired.py)
    def __getitem__(self, name):
        return LocalCollection(self._db, f"{self._coll}.{name}")

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        return LocalCollection(self._db, f"{self._coll}.{name}")

    # -- penyimpanan mentah --
    def _load_all(self):
        conn = _connect()
        rows = conn.execute(
            "SELECT doc_key, data FROM documents WHERE db=? AND collection=?",
            (self._db, self._coll),
        ).fetchall()
        return [(k, _decode(json.loads(v))) for k, v in rows]

    def _save(self, doc_key, doc):
        conn = _connect()
        conn.execute(
            "INSERT OR REPLACE INTO documents (db, collection, doc_key, data)"
            " VALUES (?, ?, ?, ?)",
            (self._db, self._coll, doc_key, json.dumps(_encode(doc))),
        )
        conn.commit()

    def _delete_key(self, doc_key):
        conn = _connect()
        conn.execute(
            "DELETE FROM documents WHERE db=? AND collection=? AND doc_key=?",
            (self._db, self._coll, doc_key),
        )
        conn.commit()

    # -- API ala motor --
    async def find_one(self, filt=None, *args, **kwargs):
        with _lock:
            for _k, doc in self._load_all():
                if _matches(doc, filt or {}):
                    return copy.deepcopy(doc)
        return None

    def find(self, filt=None, *args, **kwargs):
        with _lock:
            docs = [
                copy.deepcopy(doc)
                for _k, doc in self._load_all()
                if _matches(doc, filt or {})
            ]
        return _Cursor(docs)

    async def update_one(self, filt, update, upsert=False, **kwargs):
        filt = filt or {}
        with _lock:
            found_key, found_doc = None, None
            for k, doc in self._load_all():
                if _matches(doc, filt):
                    found_key, found_doc = k, doc
                    break
            if found_doc is None:
                if not upsert:
                    return _Result(matched=0, modified=0)
                found_doc = {
                    k: v for k, v in filt.items() if not isinstance(v, dict)
                }
                found_key = _doc_key(found_doc, filt)
            doc = copy.deepcopy(found_doc)
            if any(str(k).startswith("$") for k in update):
                for field, value in (update.get("$set") or {}).items():
                    _set_dotted(doc, field, value)
                for field in (update.get("$unset") or {}):
                    _unset_dotted(doc, field)
                for field, value in (update.get("$push") or {}).items():
                    cur = doc.get(field)
                    if not isinstance(cur, list):
                        cur = []
                    cur.append(value)
                    doc[field] = cur
                for field, value in (update.get("$pull") or {}).items():
                    cur = doc.get(field)
                    if isinstance(cur, list) and value in cur:
                        cur.remove(value)
            else:
                keep_id = doc.get("_id")
                doc = copy.deepcopy(update)
                if keep_id is not None:
                    doc["_id"] = keep_id
            self._save(_doc_key(doc, filt), doc)
            return _Result(matched=1, modified=1, upserted_id=doc.get("_id"))

    async def update_many(self, filt, update, upsert=False, **kwargs):
        docs = await self.find(filt).to_list()
        for _ in docs:
            await self.update_one(filt, update, upsert=upsert)
        return _Result(matched=len(docs), modified=len(docs))

    async def replace_one(self, filt, replacement, upsert=False, **kwargs):
        return await self.update_one(filt, {"$set": dict(replacement)}, upsert=upsert)

    async def insert_one(self, doc, **kwargs):
        with _lock:
            doc = copy.deepcopy(doc)
            self._save(_doc_key(doc), doc)
        return _Result(upserted_id=doc.get("_id"))

    async def delete_one(self, filt, **kwargs):
        with _lock:
            for k, doc in self._load_all():
                if _matches(doc, filt or {}):
                    self._delete_key(k)
                    return _Result(deleted=1)
        return _Result(deleted=0)

    async def delete_many(self, filt, **kwargs):
        count = 0
        with _lock:
            for k, doc in self._load_all():
                if _matches(doc, filt or {}):
                    self._delete_key(k)
                    count += 1
        return _Result(deleted=count)

    async def count_documents(self, filt=None, **kwargs):
        with _lock:
            return sum(1 for _k, doc in self._load_all() if _matches(doc, filt or {}))


class LocalDatabase:
    def __init__(self, name):
        object.__setattr__(self, "_name", name)

    def __getitem__(self, coll):
        return LocalCollection(self._name, coll)

    def __getattr__(self, coll):
        if coll.startswith("_"):
            raise AttributeError(coll)
        return LocalCollection(self._name, coll)


class LocalMongoClient:
    """Pengganti AsyncIOMotorClient: argumen URL apa pun diabaikan (lokal)."""

    def __init__(self, *args, **kwargs):
        pass

    def __getitem__(self, db_name):
        return LocalDatabase(db_name)

    def __getattr__(self, db_name):
        if db_name.startswith("_"):
            raise AttributeError(db_name)
        return LocalDatabase(db_name)

    def close(self):
        pass


# Nama-nama ini PERSIS sama dengan versi MongoDB, supaya semua file lain
# yang mengimpor `mongo_client` / `mongodb` tidak perlu diubah sama sekali.
mongo_client = LocalMongoClient()
mongodb = mongo_client.userbotxx

from ZallUbot.core.database.expired import *
from ZallUbot.core.database.userbot import *
from ZallUbot.core.database.pref import *
from ZallUbot.core.database.variabel import *
from ZallUbot.core.database.antigcast import *
