"""
config.py — Theme colors, font, DB path, dark mode detection.
"""

import os
import sqlite3

# ──────────────────────────────────────────────
#  DATABASE PATH
# ──────────────────────────────────────────────
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dms_database.db")


def check_dark_mode():
    try:
        c = sqlite3.connect(DB)
        cur = c.cursor()
        cur.execute("SELECT value FROM settings WHERE key='dark_mode'")
        row = cur.fetchone()
        c.close()
        return row and row[0] == "Yes"
    except Exception:
        return False


IS_DARK = check_dark_mode()

# ──────────────────────────────────────────────
#  THEME COLORS
# ──────────────────────────────────────────────
if IS_DARK:
    W    = "#1e1e1e"
    BLK  = "#f0f0f0"
    G1   = "#252526"
    G2   = "#333333"
    G3   = "#444444"
    G4   = "#888888"
    G5   = "#aaaaaa"
    ACC  = "#1a6b4a"
    ACC2 = "#145238"
    RLT  = "#3d2222"
    GLT  = "#203628"
    YLT  = "#3b351d"
    SEL  = "#2a3b4c"
else:
    W    = "#ffffff"
    BLK  = "#111111"
    G1   = "#f7f7f7"
    G2   = "#eeeeee"
    G3   = "#dddddd"
    G4   = "#999999"
    G5   = "#555555"
    ACC  = "#1a6b4a"
    ACC2 = "#145238"
    RLT  = "#fef2f2"
    GLT  = "#f0faf4"
    YLT  = "#fffbeb"
    SEL  = "#e8f4fd"

# ──────────────────────────────────────────────
#  FONT
# ──────────────────────────────────────────────
F = "Segoe UI"
