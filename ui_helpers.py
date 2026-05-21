"""
ui_helpers.py — Reusable UI widgets: styles, buttons, treeview, stat boxes, etc.
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

from config import W, BLK, G1, G2, G3, G4, G5, ACC, ACC2, GLT, YLT, SEL, F, IS_DARK


def setup_styles():
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("M.Treeview",
        background=W, foreground=BLK,
        fieldbackground=W, rowheight=30,
        font=(F, 9), borderwidth=0)
    s.configure("M.Treeview.Heading",
        background=ACC, foreground="#ffffff",
        font=(F, 9, "bold"), relief="flat", padding=9)
    s.map("M.Treeview",
        background=[("selected", SEL)],
        foreground=[("selected", BLK)])
    s.configure("TCombobox",
        fieldbackground=G2, background=G2,
        foreground=BLK, bordercolor=G3, relief="flat")
    s.map("TCombobox",
        fieldbackground=[("readonly", G2)],
        foreground=[("readonly", BLK)])
    s.configure("TScrollbar",
        background=G2, troughcolor=G1,
        borderwidth=0, arrowsize=14)


def mk_btn(parent, text, cmd, style="p", px=14, py=7, side=None):
    cfg = {
        "p": (ACC,       "#ffffff", ACC2),
        "d": ("#b91c1c", "#ffffff", "#991b1b"),
        "s": (G2,        BLK,       G3),
        "w": ("#b45309", "#ffffff", "#92400e"),
        "t": ("#0f766e", "#ffffff", "#0d5e57"),
    }
    bg, fg, abg = cfg.get(style, cfg["p"])
    b = tk.Button(parent, text=text, command=cmd, bg=bg, fg=fg,
                  relief=tk.FLAT, font=(F, 10, "bold"),
                  padx=px, pady=py, cursor="hand2",
                  activebackground=abg, activeforeground=fg, bd=0)
    if side:
        b.pack(side=side, padx=3, pady=2)
    return b


def mk_tree(parent, cols, widths, height=8):
    frm = tk.Frame(parent, bg=W, bd=1, relief=tk.SOLID)
    tv  = ttk.Treeview(frm, columns=cols, show="headings",
                       height=height, style="M.Treeview")
    for c, w in zip(cols, widths):
        tv.heading(c, text=c)
        tv.column(c, width=w, anchor=tk.CENTER, minwidth=30, stretch=False)
    tv.column(cols[2], stretch=True)  # Subject/3rd column stretches
    tv.tag_configure("IN",  background="#f2fdf7", foreground="#111111")
    tv.tag_configure("OUT", background="#fff7f7", foreground="#111111")
    tv.tag_configure("urg", font=(F, 9, "bold"))
    tv.tag_configure("ovr", background=YLT)
    tv.tag_configure("alt", background=G1)
    vsb = ttk.Scrollbar(frm, orient="vertical",   command=tv.yview)
    hsb = ttk.Scrollbar(frm, orient="horizontal", command=tv.xview)
    tv.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.pack(side=tk.RIGHT,  fill=tk.Y)
    hsb.pack(side=tk.BOTTOM, fill=tk.X)
    tv.pack(fill=tk.BOTH, expand=True)
    return frm, tv


def divider(parent, pady=8):
    tk.Frame(parent, bg=G3, height=1).pack(fill=tk.X, pady=pady)


def stat_box(parent, col, title, val, tint=G1):
    f = tk.Frame(parent, bg=tint, bd=1, relief=tk.SOLID)
    f.grid(row=0, column=col, padx=5, pady=5,
           sticky="nsew", ipadx=10, ipady=8)
    parent.columnconfigure(col, weight=1)
    tk.Label(f, text=str(val), font=(F, 26, "bold"),
             bg=tint, fg=BLK).pack()
    tk.Label(f, text=title, font=(F, 8),
             bg=tint, fg=G5).pack()


def open_file(path):
    if not path or not os.path.exists(path):
        messagebox.showwarning("File Not Found", f"File not found:\n{path}")
        return
    try:
        if sys.platform == "win32":    os.startfile(path)
        elif sys.platform == "darwin": subprocess.Popen(["open", path])
        else:                          subprocess.Popen(["xdg-open", path])
    except Exception as e:
        messagebox.showerror("Error", str(e))
