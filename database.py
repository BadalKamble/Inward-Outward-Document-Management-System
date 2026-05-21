"""
database.py — Database layer: init, helpers, queries.
"""

import sqlite3
import datetime
import hashlib

from config import DB


def con():
    return sqlite3.connect(DB)

def hp(p):
    return hashlib.sha256(p.encode()).hexdigest()

def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def tod():
    return datetime.date.today().strftime("%Y-%m-%d")


def init_db():
    c = con()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS users(
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        username    TEXT UNIQUE NOT NULL,
        password    TEXT NOT NULL,
        full_name   TEXT DEFAULT '',
        email       TEXT DEFAULT '',
        phone       TEXT DEFAULT '',
        department  TEXT DEFAULT '',
        role        TEXT DEFAULT 'User',
        is_active   INTEGER DEFAULT 1,
        last_login  TEXT DEFAULT '',
        created_at  TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS documents(
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_type        TEXT NOT NULL,
        doc_no          TEXT UNIQUE NOT NULL,
        subject         TEXT NOT NULL,
        sender_receiver TEXT NOT NULL,
        department      TEXT DEFAULT '',
        forwarded_to    TEXT DEFAULT '',
        date_entry      TEXT NOT NULL,
        doc_date        TEXT DEFAULT '',
        due_date        TEXT DEFAULT '',
        priority        TEXT DEFAULT 'Normal',
        status          TEXT DEFAULT 'Pending',
        remarks         TEXT DEFAULT '',
        file_path       TEXT DEFAULT '',
        tags            TEXT DEFAULT '',
        ref_no          TEXT DEFAULT '',
        created_by      TEXT DEFAULT '',
        updated_at      TEXT DEFAULT '',
        created_at      TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS doc_history(
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_id      INTEGER NOT NULL,
        action      TEXT NOT NULL,
        old_value   TEXT DEFAULT '',
        new_value   TEXT DEFAULT '',
        field_name  TEXT DEFAULT 'status',
        remarks     TEXT DEFAULT '',
        done_by     TEXT DEFAULT '',
        done_at     TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS settings(
        key   TEXT PRIMARY KEY,
        value TEXT DEFAULT ''
    );
    """)

    # default admin
    c.execute("""INSERT OR IGNORE INTO users
        (username,password,full_name,email,department,role,is_active,created_at)
        VALUES(?,?,?,?,?,?,1,?)""",
        ("admin", hp("admin123"), "Administrator",
         "admin@company.com", "Administration", "Admin", now()))

    # default clerk
    c.execute("""INSERT OR IGNORE INTO users
        (username,password,full_name,email,department,role,is_active,created_at)
        VALUES(?,?,?,?,?,?,1,?)""",
        ("clerk", hp("clerk123"), "Office Clerk",
         "clerk@company.com", "Administration", "Clerk", now()))

    # default user
    c.execute("""INSERT OR IGNORE INTO users
        (username,password,full_name,email,department,role,is_active,created_at)
        VALUES(?,?,?,?,?,?,1,?)""",
        ("user", hp("user123"), "General User",
         "user@company.com", "General", "User", now()))

    # default settings
    for k, v in [("org_name", "My Organization"), ("dark_mode", "No"),
                 ("default_export", "CSV"), ("dash_rows", "10")]:
        c.execute("INSERT OR IGNORE INTO settings(key,value) VALUES(?,?)", (k, v))

    c.commit()
    c.close()


def next_no(doc_type):
    yr = datetime.datetime.now().strftime("%Y")
    px = "IN" if doc_type == "INWARD" else "OUT"
    c = con(); cur = c.cursor()
    cur.execute("SELECT COUNT(*) FROM documents WHERE doc_type=? AND created_at LIKE ?",
                (doc_type, yr + "%"))
    n = cur.fetchone()[0] + 1
    c.close()
    return f"{px}/{yr}/{n:04d}"


def audit(doc_id, action, old_val, new_val, field, remark, user):
    c = con()
    c.execute("INSERT INTO doc_history"
              "(doc_id,action,old_value,new_value,field_name,remarks,done_by,done_at)"
              " VALUES(?,?,?,?,?,?,?,?)",
              (doc_id, action, old_val or "", new_val or "",
               field or "status", remark or "", user, now()))
    c.commit()
    c.close()


def get_setting(key, default=""):
    c = con(); cur = c.cursor()
    cur.execute("SELECT value FROM settings WHERE key=?", (key,))
    row = cur.fetchone()
    c.close()
    return row[0] if row else default


def can_edit(role):
    """Returns True if role is allowed to edit/delete documents."""
    return role in ("Admin", "Clerk")
