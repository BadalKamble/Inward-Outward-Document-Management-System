"""
main.py — Entry point for the Document Management System.

Run this file to start the application:
    python main.py

File Structure:
    main.py          ← Entry point (this file)
    config.py        ← Theme colors, DB path, dark mode detection
    database.py      ← DB init, queries, helper functions
    ui_helpers.py    ← Reusable UI widgets (buttons, treeview, etc.)
    dialogs.py       ← Popup dialogs (User add/edit, password, history)
    app_windows.py   ← LoginWin + AppWin (all pages)
"""

from app_windows import LoginWin

if __name__ == "__main__":
    app = LoginWin()
    app.mainloop()
