"""
dialogs.py — Popup dialogs: HistWin, PrintWin, UserDlg, UserEditDlg, ChangePwDlg.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from config import W, BLK, G1, G2, G3, G4, G5, ACC, ACC2, F
from database import con, hp, now, audit
from ui_helpers import mk_btn, mk_tree


# ══════════════════════════════════════════════════════════
#  DOCUMENT HISTORY POPUP
# ══════════════════════════════════════════════════════════
class HistWin(tk.Toplevel):
    def __init__(self, parent, doc_id):
        super().__init__(parent)
        self.title("Document History")
        self.geometry("800x430")
        self.configure(bg=W)
        self.grab_set()

        tk.Frame(self, bg=ACC, height=44).pack(fill=tk.X)

        c = con(); cur = c.cursor()
        cur.execute("SELECT doc_no,subject FROM documents WHERE id=?", (doc_id,))
        doc = cur.fetchone() or ("?", "?")
        tk.Label(self, text=f"History:  {doc[0]}  —  {doc[1][:52]}",
                 font=(F, 11, "bold"), bg=W, fg=BLK).pack(pady=10, padx=16, anchor="w")

        frm, tv = mk_tree(self,
            ("Action", "Field", "Old Value", "New Value", "Remarks", "Done By", "Date/Time"),
            [90, 80, 120, 120, 240, 110, 150], height=14)
        frm.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 6))

        cur.execute("SELECT action,field_name,old_value,new_value,remarks,done_by,done_at "
                    "FROM doc_history WHERE doc_id=? ORDER BY id DESC", (doc_id,))
        for i, row in enumerate(cur.fetchall()):
            tv.insert("", "end", values=row, tags=("alt" if i % 2 else "",))
        c.close()

        mk_btn(self, "  Close  ", self.destroy, style="s", py=6).pack(pady=8)


# ══════════════════════════════════════════════════════════
#  DOCUMENT PRINT/RECEIPT WINDOW
# ══════════════════════════════════════════════════════════
class PrintWin(tk.Toplevel):
    def __init__(self, parent, row, hdrs, user):
        super().__init__(parent)
        self.title("Print Receipt")
        self.geometry("620x720")
        self.configure(bg=W)
        self.grab_set()

        hdr = tk.Frame(self, bg=ACC, height=68)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        tk.Label(hdr, text="DOCUMENT RECEIPT", font=(F, 16, "bold"),
                 bg=ACC, fg="#ffffff").pack(pady=(14, 0))

        tk.Frame(self, bg=G3, height=1).pack(fill=tk.X, padx=28, pady=(14, 8))

        card2 = tk.Frame(self, bg=W)
        card2.pack(fill=tk.BOTH, padx=28)
        card2.columnconfigure(1, weight=1)

        show = {"doc_type", "doc_no", "subject", "sender_receiver", "department",
                "forwarded_to", "date_entry", "doc_date", "due_date",
                "priority", "status", "tags", "ref_no", "remarks", "created_by", "created_at"}
        ri = 0
        for h, v in zip(hdrs, row):
            if h not in show:
                continue
            tk.Label(card2, text=h.replace("_", " ").title() + ":",
                     font=(F, 9, "bold"), bg=W, fg=BLK, anchor="w").grid(
                     row=ri, column=0, sticky="w", padx=(0, 10), pady=(4, 0))
            tk.Label(card2, text=str(v or "—"),
                     font=(F, 9), bg=W, fg=BLK, anchor="w",
                     wraplength=360, justify=tk.LEFT).grid(
                     row=ri, column=1, sticky="w", pady=(4, 0))
            ri += 1

        tk.Frame(self, bg=G3, height=1).pack(fill=tk.X, padx=28, pady=12)
        tk.Label(self, text=f"Printed: {now()}", font=(F, 8), bg=W, fg=G4).pack()
        mk_btn(self, "  Close  ", self.destroy, style="s", py=6).pack(pady=12)


# ══════════════════════════════════════════════════════════
#  ADD NEW USER DIALOG
# ══════════════════════════════════════════════════════════
class UserDlg(tk.Toplevel):
    def __init__(self, parent, user_row, on_done):
        super().__init__(parent)
        self.on_done = on_done
        self.eid = user_row[0] if user_row else None
        self.title("Add New User")
        self.geometry("480x620")
        self.resizable(False, False)
        self.configure(bg=W)
        self.grab_set()

        tk.Frame(self, bg=ACC, height=48).pack(fill=tk.X)
        tk.Label(self, text="Add New User", font=(F, 14, "bold"), bg=W, fg=BLK).pack(pady=(14, 4))
        tk.Label(self, text="Fill all required fields (*) to create a new user.",
                 font=(F, 9), bg=W, fg=G4).pack(pady=(0, 6))

        card = tk.Frame(self, bg=W, padx=30)
        card.pack(fill=tk.X)
        card.columnconfigure(0, weight=1)

        def fld(lbl, row_n, val="", show=""):
            tk.Label(card, text=lbl, font=(F, 9, "bold"), bg=W, fg=BLK).grid(
                row=row_n * 2, column=0, sticky="w", pady=(8, 1))
            wrap = tk.Frame(card, bg=G3)
            wrap.grid(row=row_n * 2 + 1, column=0, sticky="ew", pady=(0, 2))
            e = tk.Entry(wrap, show=show, bg=G2, fg=BLK, insertbackground=BLK,
                         relief=tk.FLAT, font=(F, 10), bd=7)
            e.pack(fill=tk.X)
            if val:
                e.insert(0, val)
            return e

        self._eu    = fld("Username *",  0)
        self._efn   = fld("Full Name *", 1)
        self._epw   = fld("Password *",  2, show="*")
        self._eeml  = fld("Email",       3)
        self._edept = fld("Department",  4)

        tk.Label(card, text="Role *", font=(F, 9, "bold"), bg=W, fg=BLK).grid(
            row=10, column=0, sticky="w", pady=(8, 1))
        self._vr = tk.StringVar(value="User")
        rw = tk.Frame(card, bg=G3)
        rw.grid(row=11, column=0, sticky="ew", pady=(0, 2))
        ttk.Combobox(rw, textvariable=self._vr,
                     values=["User", "Clerk", "Manager", "Admin"],
                     width=36, font=(F, 10), state="readonly").pack(fill=tk.X, ipady=5)

        self._em2 = tk.StringVar()
        tk.Label(self, textvariable=self._em2, font=(F, 9), bg=W, fg="#b91c1c").pack(pady=(6, 0))

        bf = tk.Frame(self, bg=W)
        bf.pack(pady=12)
        mk_btn(bf, "  Save User  ", self._save, style="p", side=tk.LEFT)
        mk_btn(bf, "  Cancel  ",   self.destroy, style="s", side=tk.LEFT)

    def _save(self):
        u    = self._eu.get().strip()
        fn   = self._efn.get().strip()
        p    = self._epw.get()
        eml  = self._eeml.get().strip()
        dept = self._edept.get().strip()
        role = self._vr.get()

        if not u:
            self._em2.set("Username is required!"); return
        if not fn:
            self._em2.set("Full Name is required!"); return
        if len(p) < 6:
            self._em2.set("Password must be at least 6 characters!"); return
        try:
            import sqlite3
            c = con()
            c.execute("""INSERT INTO users
                (username, password, full_name, email, phone, department, role, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?)""",
                (u, hp(p), fn, eml, "", dept, role, now()))
            c.commit(); c.close()
            self.on_done()
            self.destroy()
            messagebox.showinfo("Success", f"User '{u}' added successfully!")
        except sqlite3.IntegrityError:
            self._em2.set(f"Username '{u}' already exists!")


# ══════════════════════════════════════════════════════════
#  EDIT USER DIALOG
# ══════════════════════════════════════════════════════════
class UserEditDlg(tk.Toplevel):
    """Edit existing user — Full Name, Email, Department, Role."""
    def __init__(self, parent, user_row, on_done, current_user=None):
        super().__init__(parent)
        self.on_done = on_done
        self.uid = user_row[0]
        self.current_user = current_user
        self.target_username = user_row[1]
        self.target_role = user_row[7] or "User"
        self.title("Edit User")
        self.geometry("460x540")
        self.resizable(False, False)
        self.configure(bg=W)
        self.grab_set()

        tk.Frame(self, bg=ACC, height=44).pack(fill=tk.X)
        tk.Label(self, text=f"Edit User: {user_row[1]}",
                 font=(F, 14, "bold"), bg=W, fg=BLK).pack(pady=(14, 10))

        card = tk.Frame(self, bg=W, padx=28)
        card.pack(fill=tk.BOTH, expand=True)
        card.columnconfigure(0, weight=1)

        def fld(lbl, row_n, val=""):
            tk.Label(card, text=lbl, font=(F, 9, "bold"), bg=W, fg=BLK).grid(
                row=row_n * 2, column=0, sticky="w", pady=(8, 1))
            wrap = tk.Frame(card, bg=G3)
            wrap.grid(row=row_n * 2 + 1, column=0, sticky="ew", pady=(0, 2))
            e = tk.Entry(wrap, bg=G2, fg=BLK, insertbackground=BLK,
                         relief=tk.FLAT, font=(F, 10), bd=7)
            e.pack(fill=tk.X)
            if val:
                e.insert(0, val)
            return e

        self._efn   = fld("Full Name",  0, user_row[3] or "")
        self._eeml  = fld("Email",      1, user_row[4] or "")
        self._edept = fld("Department", 2, user_row[6] or "")

        # Admin cannot change their own role (prevent accidental lockout)
        is_own_account = (current_user and
                          current_user.get("username") == self.target_username)
        role_locked = is_own_account and self.target_role == "Admin"

        tk.Label(card, text="Role", font=(F, 9, "bold"), bg=W, fg=BLK).grid(
            row=6, column=0, sticky="w", pady=(8, 1))
        self._vr = tk.StringVar(value=self.target_role)
        rw = tk.Frame(card, bg=G3)
        rw.grid(row=7, column=0, sticky="ew", pady=(0, 2))
        role_state = "disabled" if role_locked else "readonly"
        ttk.Combobox(rw, textvariable=self._vr,
                     values=["User", "Clerk", "Manager", "Admin"],
                     width=36, font=(F, 10), state=role_state).pack(fill=tk.X, ipady=5)

        if role_locked:
            tk.Label(card, text="⚠ You cannot change your own Admin role.",
                     font=(F, 8), bg=W, fg="#b45309").grid(
                     row=8, column=0, sticky="w", pady=(2, 0))

        self._emsg = tk.StringVar()
        tk.Label(self, textvariable=self._emsg, font=(F, 9), bg=W, fg="#b91c1c").pack(pady=(4, 0))

        bf = tk.Frame(self, bg=W)
        bf.pack(pady=12)
        mk_btn(bf, "  Save Changes  ", self._save, style="p", side=tk.LEFT)
        mk_btn(bf, "  Cancel  ",       self.destroy, style="s", side=tk.LEFT)

    def _save(self):
        fn   = self._efn.get().strip()
        eml  = self._eeml.get().strip()
        dept = self._edept.get().strip()
        role = self._vr.get()

        # Server-side guard: Admin cannot change their own role
        is_own_account = (self.current_user and
                          self.current_user.get("username") == self.target_username)
        if is_own_account and self.target_role == "Admin" and role != "Admin":
            self._emsg.set("You cannot change your own Admin role!")
            return

        c = con()
        c.execute("""UPDATE users SET full_name=?,email=?,department=?,role=?
                     WHERE id=?""", (fn, eml, dept, role, self.uid))
        c.commit(); c.close()
        messagebox.showinfo("Saved", "User details updated successfully!")
        self.on_done()
        self.destroy()


# ══════════════════════════════════════════════════════════
#  CHANGE PASSWORD DIALOG
# ══════════════════════════════════════════════════════════
class ChangePwDlg(tk.Toplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.user_id = user_id
        self.title("Change Password")
        self.geometry("400x400")
        self.configure(bg=W)
        self.grab_set()

        tk.Frame(self, bg=ACC, height=44).pack(fill=tk.X)
        tk.Label(self, text="Change Password",
                 font=(F, 14, "bold"), bg=W, fg=BLK).pack(pady=(14, 10))

        frm = tk.Frame(self, bg=W, padx=25)
        frm.pack(fill=tk.BOTH, expand=True)

        def pwf(lbl):
            tk.Label(frm, text=lbl, font=(F, 9, "bold"), bg=W, fg=BLK).pack(anchor="w", pady=(8, 2))
            wrap = tk.Frame(frm, bg=G3)
            wrap.pack(fill=tk.X, pady=(0, 4))
            e = tk.Entry(wrap, show="*", bg=G2, fg=BLK, insertbackground=BLK,
                         relief=tk.FLAT, font=(F, 10), bd=7)
            e.pack(fill=tk.X)
            return e

        self.e_old = pwf("Current Password")
        self.e_n1  = pwf("New Password")
        self.e_n2  = pwf("Confirm New Password")

        self.pmsg = tk.StringVar()
        tk.Label(frm, textvariable=self.pmsg, font=(F, 9), bg=W, fg="#b91c1c").pack(pady=(10, 0))
        mk_btn(frm, "  Update Password  ", self.chg, style="p", py=9, px=0).pack(fill=tk.X, pady=(15, 0))

    def chg(self):
        c = con(); cur = c.cursor()
        cur.execute("SELECT password FROM users WHERE id=?", (self.user_id,))
        row = cur.fetchone(); c.close()
        if not row or row[0] != hp(self.e_old.get()):
            self.pmsg.set("Incorrect current password!"); return
        if len(self.e_n1.get()) < 6:
            self.pmsg.set("New password must be 6+ characters!"); return
        if self.e_n1.get() != self.e_n2.get():
            self.pmsg.set("Passwords do not match!"); return
        c = con()
        c.execute("UPDATE users SET password=? WHERE id=?", (hp(self.e_n1.get()), self.user_id))
        c.commit(); c.close()
        messagebox.showinfo("Done", "Password changed successfully!")
        self.destroy()
