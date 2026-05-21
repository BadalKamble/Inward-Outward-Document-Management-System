📂 IODMS — Inward Outward Document Management System

Desktop Application | Python · Tkinter · SQLite | Role-Based Access Control


📌 Project Title
IODMS — Inward/Outward Document Management System

📝 Short Description
A fully functional desktop-based Document Management System built with Python and Tkinter. IODMS digitizes the traditional inward/outward document register used in offices and organizations — enabling clerks and admins to log, track, search, and manage documents with auto-generated document numbers, role-based access control, audit history, and dark mode support.

🎯 Purpose
This project was built to:

Replace manual paper-based inward/outward registers with a digital system
Implement role-based access (Admin, Clerk, User) for document security
Practice Business Analyst skills — requirements gathering, stakeholder identification, process documentation, and system design
Demonstrate real-world Python desktop application development with database integration


🛠️ Tech Stack
Tool / TechnologyUsagePython 3.xCore application logicTkinter + ttkDesktop GUI frameworkSQLite3Local database (dms_database.db)Hashlib (SHA-256)Secure password hashingdatetime / osDate handling and file paths

📁 Project Structure
IODMS/
│
├── main.py          ← Entry point — run this to start the app
├── config.py        ← Theme colors, DB path, dark mode detection
├── database.py      ← DB init, queries, helper functions
├── ui_helpers.py    ← Reusable UI widgets (buttons, treeview, stat boxes)
├── dialogs.py       ← Popup dialogs (User add/edit, password, history)
├── app_windows.py   ← LoginWin + AppWin (all pages/screens)
└── dms_database.db  ← SQLite database (auto-created on first run)

✨ Features & Highlights
🔐 Role-Based Access Control
Three roles with different permissions:

Admin — Full access: manage users, documents, settings
Clerk — Can add, edit, delete documents
User — Read-only: view and search documents only


📋 Document Management (CRUD)

Add, edit, delete Inward and Outward documents
Fields: Subject, Sender/Receiver, Department, Forwarded To, Priority, Status, Due Date, Tags, Remarks, File Attachment

🔍 Advanced Search & Filters

Search by document number, subject, sender, department, tags
Filter by type, status, priority, and date range

📜 Audit Trail / Document History

Every change (edit, status update) is logged automatically
Full history popup showing old value → new value with timestamp and user

👥 User Management (Admin Only)

Add new users with username, password, role, department
Edit user details and role assignments
Change password with current password verification
Admin cannot accidentally remove their own Admin role (lockout prevention)

🌗 Dark Mode Support

Toggle between light and dark theme stored in settings table
All UI colors adapt automatically via config.py

📊 Dashboard Stats

Summary stat boxes showing total inward, outward, pending, and urgent documents

🖨️ Print Receipt

Generate a formatted document receipt/printout from any record


🚀 How to Run
bash# 1. Clone the repository
git clone https://github.com/YOUR-USERNAME/IODMS.git
cd IODMS

# 2. Install dependencies (only standard library used)
# No pip install needed — Python 3.x is sufficient

# 3. Run the application
python main.py
Default Login Credentials:
UsernamePasswordRoleadminadmin123Adminclerkclerk123Clerkuseruser123User

Default Login Credentials:
Role         Username           Password
admin        admin              admin123
clerk        clerk              clerk123
user         user               user123 


💡 Key Insights & BA Perspective

Identified 3 stakeholder types (Admin, Clerk, User) and mapped permissions accordingly
Designed auto-numbering system to prevent duplicate document entries
Implemented audit trail to meet organizational accountability requirements
Dark mode and modular architecture make the system maintainable and extensible


🎓 About
Developed as a major project during my BCA studies and extended as a core Business Analyst portfolio piece — demonstrating requirements gathering, system design, and full-cycle desktop application development.
Developer: Badal
Education: BCA — Dayanand College of Commerce, Latur (SRTMU)
