import os
import sqlite3
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller bundle."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# --- OFFICIAL IITH BRAND COLOR PALETTE ---
IITH_NAVY = "#00188F"
IITH_RED = "#E50C0C"
IITH_ORANGE = "#FF7B00"
IITH_YELLOW = "#FFC000"
IITH_LIGHT_BG = "#F4F6F9"
IITH_CARD = "#FFFFFF"

# Status Colors
COLOR_EMPTY = "#28A745"
COLOR_FULL = "#DC3545"
COLOR_MAINTENANCE = "#FF7B00"
COLOR_MATCH = "#8E44AD"
COLOR_NSO = "#00A8CC"
COLOR_INTER_IIT = "#00188F"


def get_db_connection():
    return sqlite3.connect("sncc_badminton.db")


def initialize_db():
    try:
        con = get_db_connection()
        cur = con.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS badminton (
                Court_No INTEGER PRIMARY KEY,
                availability TEXT DEFAULT 'EMPTY'
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS court_queue (
                queue_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                roll_no TEXT NOT NULL,
                court_no INTEGER NOT NULL
            )
        """)

        cur.execute(
            "INSERT OR IGNORE INTO badminton(Court_No) VALUES (1), (2), (3),"
            " (4)"
        )
        cur.execute("""
            INSERT OR IGNORE INTO staff VALUES 
            (260089, 'Ramesh'),
            (250076, 'Mahesh'),
            (240053, 'Shivesh')
        """)

        con.commit()
        con.close()
    except Exception as e:
        print(f"Database initialization error: {e}")


initialize_db()

# --- MAIN WINDOW SETUP ---
root = tk.Tk()
root.title("IIT Hyderabad - SNCC Badminton Portal")
root.geometry("850x700")
root.configure(bg=IITH_LIGHT_BG)

# Enable Resizing & Open Maximized
root.resizable(True, True)
try:
    root.state("zoomed")  # Maximizes on Windows
except Exception:
    root.attributes("-zoomed", True)  # Maximizes on Linux/macOS

# --- STYLES ---
style = ttk.Style()
style.theme_use("clam")

style.configure("TNotebook", background=IITH_LIGHT_BG, borderwidth=0)
style.configure(
    "TNotebook.Tab",
    font=("Helvetica", 10, "bold"),
    padding=[18, 8],
    background="#E2E8F0",
    foreground=IITH_NAVY,
)
style.map(
    "TNotebook.Tab",
    background=[("selected", IITH_NAVY)],
    foreground=[("selected", "#FFFFFF")],
)

style.configure(
    "Treeview",
    font=("Helvetica", 10),
    rowheight=30,
    background=IITH_CARD,
    fieldbackground=IITH_CARD,
)
style.configure(
    "Treeview.Heading",
    font=("Helvetica", 10, "bold"),
    background=IITH_NAVY,
    foreground="#FFFFFF",
)

style.configure(
    "Primary.TButton",
    font=("Helvetica", 10, "bold"),
    background=IITH_RED,
    foreground="#FFFFFF",
    borderwidth=0,
)
style.map("Primary.TButton", background=[("active", "#B30000")])

style.configure(
    "Secondary.TButton",
    font=("Helvetica", 10, "bold"),
    background=IITH_NAVY,
    foreground="#FFFFFF",
    borderwidth=0,
)
style.map("Secondary.TButton", background=[("active", "#000D55")])


# ================= HEADER =================
header_frame = tk.Frame(root, bg=IITH_NAVY, height=85)
header_frame.pack(fill="x", side="top")
header_frame.pack_propagate(False)

try:
    logo_path = resource_path("iith_logo.png")
    logo_img = Image.open(logo_path)
    logo_img = logo_img.resize((58, 58), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(header_frame, image=logo_photo, bg=IITH_NAVY)
    logo_label.image = logo_photo
    logo_label.pack(side="left", padx=(15, 10), pady=12)
except Exception:
    pass

header_text_frame = tk.Frame(header_frame, bg=IITH_NAVY)
header_text_frame.pack(side="left", fill="y", pady=16)

tk.Label(
    header_text_frame,
    text="IIT HYDERABAD",
    font=("Helvetica", 14, "bold"),
    bg=IITH_NAVY,
    fg="#FFFFFF",
).pack(anchor="w")
tk.Label(
    header_text_frame,
    text="SNCC Badminton Court Portal",
    font=("Helvetica", 10),
    bg=IITH_NAVY,
    fg=IITH_YELLOW,
).pack(anchor="w")

tk.Label(
    header_frame,
    text="🏸",
    font=("Segoe UI Emoji", 28),
    bg=IITH_NAVY,
    fg="#FFFFFF",
).pack(side="right", padx=20)

# Brand Stripe
stripe_frame = tk.Frame(root, height=5, bg=IITH_LIGHT_BG)
stripe_frame.pack(fill="x", side="top")
tk.Frame(stripe_frame, bg=IITH_RED, height=5).pack(
    side="left", expand=True, fill="both"
)
tk.Frame(stripe_frame, bg=IITH_ORANGE, height=5).pack(
    side="left", expand=True, fill="both"
)
tk.Frame(stripe_frame, bg=IITH_YELLOW, height=5).pack(
    side="left", expand=True, fill="both"
)


# ================= TABS CONTAINER =================
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=20, pady=15)

student_tab = tk.Frame(notebook, bg=IITH_CARD)
staff_tab = tk.Frame(notebook, bg=IITH_CARD)

notebook.add(student_tab, text="Student View & Queue")
notebook.add(staff_tab, text="Staff Portal")


# ================= TAB 1: STUDENT VIEW =================
student_container = tk.Frame(student_tab, bg=IITH_CARD, padx=15, pady=15)
student_container.pack(fill="both", expand=True)

# Grid expansion setup
student_container.columnconfigure(0, weight=1)
student_container.rowconfigure(1, weight=1)
student_container.rowconfigure(3, weight=1)

tk.Label(
    student_container,
    text="Current Court Availability",
    font=("Helvetica", 11, "bold"),
    bg=IITH_CARD,
    fg=IITH_NAVY,
).grid(row=0, column=0, sticky="w", pady=(0, 5))

court_tree = ttk.Treeview(
    student_container,
    columns=("Court", "Status", "Queue"),
    show="headings",
    height=4,
)
court_tree.heading("Court", text="Court No")
court_tree.heading("Status", text="Status")
court_tree.heading("Queue", text="Waiting in Queue")
court_tree.column("Court", anchor="center", width=120)
court_tree.column("Status", anchor="center", width=220)
court_tree.column("Queue", anchor="center", width=200)
court_tree.grid(row=1, column=0, sticky="nsew", pady=(0, 15))

court_tree.tag_configure(
    "EMPTY", foreground=COLOR_EMPTY, font=("Helvetica", 10, "bold")
)
court_tree.tag_configure(
    "FULL", foreground=COLOR_FULL, font=("Helvetica", 10, "bold")
)
court_tree.tag_configure(
    "MAINTENANCE", foreground=COLOR_MAINTENANCE, font=("Helvetica", 10, "bold")
)
court_tree.tag_configure(
    "OFFICIAL MATCH", foreground=COLOR_MATCH, font=("Helvetica", 10, "bold")
)
court_tree.tag_configure(
    "NSO Practice", foreground=COLOR_NSO, font=("Helvetica", 10, "bold")
)
court_tree.tag_configure(
    "Inter-IIT Practice",
    foreground=COLOR_INTER_IIT,
    font=("Helvetica", 10, "bold"),
)

tk.Label(
    student_container,
    text="Live Waiting Queue",
    font=("Helvetica", 11, "bold"),
    bg=IITH_CARD,
    fg=IITH_NAVY,
).grid(row=2, column=0, sticky="w", pady=(0, 5))

queue_tree = ttk.Treeview(
    student_container,
    columns=("Pos", "Court", "Name", "RollNo"),
    show="headings",
    height=4,
)
queue_tree.heading("Pos", text="Pos #")
queue_tree.heading("Court", text="Court")
queue_tree.heading("Name", text="Student Name")
queue_tree.heading("RollNo", text="Roll Number")
queue_tree.column("Pos", anchor="center", width=80)
queue_tree.column("Court", anchor="center", width=100)
queue_tree.column("Name", anchor="w", width=250)
queue_tree.column("RollNo", anchor="center", width=200)
queue_tree.grid(row=3, column=0, sticky="nsew", pady=(0, 15))


def fetch_courts_and_queue():
    for row in court_tree.get_children():
        court_tree.delete(row)
    for row in queue_tree.get_children():
        queue_tree.delete(row)

    try:
        con = get_db_connection()
        cur = con.cursor()

        cur.execute("""
            SELECT b.Court_No, b.availability, COUNT(q.queue_id) 
            FROM badminton b 
            LEFT JOIN court_queue q ON b.Court_No = q.court_no 
            GROUP BY b.Court_No, b.availability 
            ORDER BY b.Court_No ASC
        """)
        for court, status, q_count in cur.fetchall():
            q_text = f"{q_count} Waiting" if q_count > 0 else "No Queue"
            court_tree.insert(
                "",
                "end",
                values=(f"Court {court}", status, q_text),
                tags=(status,),
            )

        cur.execute(
            "SELECT court_no, student_name, roll_no FROM court_queue ORDER BY"
            " queue_id ASC"
        )
        for pos, (c_no, s_name, r_no) in enumerate(cur.fetchall(), start=1):
            queue_tree.insert(
                "", "end", values=(f"#{pos}", f"Court {c_no}", s_name, r_no)
            )

        con.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not fetch data:\n{e}")


# Join Queue Card
queue_card = tk.LabelFrame(
    student_container,
    text=" ➕ Join Court Waiting Queue ",
    font=("Helvetica", 10, "bold"),
    bg=IITH_CARD,
    fg=IITH_NAVY,
    padx=15,
    pady=10,
)
queue_card.grid(row=4, column=0, sticky="ew", pady=(0, 10))

tk.Label(queue_card, text="Name:", bg=IITH_CARD, font=("Helvetica", 10)).grid(
    row=0, column=0, sticky="w"
)
student_name_entry = ttk.Entry(queue_card, font=("Helvetica", 10))
student_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

tk.Label(
    queue_card, text="Roll No:", bg=IITH_CARD, font=("Helvetica", 10)
).grid(row=0, column=2, sticky="w")
student_roll_entry = ttk.Entry(queue_card, font=("Helvetica", 10))
student_roll_entry.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

tk.Label(queue_card, text="Court:", bg=IITH_CARD, font=("Helvetica", 10)).grid(
    row=1, column=0, sticky="w"
)
q_court_combo = ttk.Combobox(
    queue_card, values=[1, 2, 3, 4], state="readonly", font=("Helvetica", 10)
)
q_court_combo.set(1)
q_court_combo.grid(row=1, column=1, padx=10, pady=5, sticky="ew")


def join_queue():
    name = student_name_entry.get().strip()
    roll = student_roll_entry.get().strip()
    court = q_court_combo.get()

    if not name or not roll:
        messagebox.showwarning(
            "Input Error", "Please enter both Name and Roll Number!"
        )
        return

    try:
        con = get_db_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO court_queue (student_name, roll_no, court_no) VALUES"
            " (?, ?, ?)",
            (name, roll, court),
        )
        con.commit()
        con.close()

        messagebox.showinfo(
            "Queue Joined",
            f"Successfully added {name} to Court {court} queue!",
        )
        student_name_entry.delete(0, tk.END)
        student_roll_entry.delete(0, tk.END)
        fetch_courts_and_queue()
    except Exception as e:
        messagebox.showerror("Database Error", f"Could not join queue:\n{e}")


ttk.Button(
    queue_card, text="Join Queue", style="Secondary.TButton", command=join_queue
).grid(row=1, column=2, columnspan=2, sticky="ew", padx=10, pady=5)

queue_card.columnconfigure(1, weight=1)
queue_card.columnconfigure(3, weight=1)

ttk.Button(
    student_container,
    text="🔄 Refresh Status & Queue",
    style="Primary.TButton",
    command=fetch_courts_and_queue,
).grid(row=5, column=0, sticky="ew")


# ================= TAB 2: STAFF PORTAL =================
staff_container = tk.Frame(staff_tab, bg=IITH_CARD, padx=30, pady=20)
staff_container.pack(fill="both", expand=True)

tk.Label(
    staff_container,
    text="Staff ID Authentication",
    font=("Helvetica", 11, "bold"),
    bg=IITH_CARD,
    fg=IITH_NAVY,
).pack(anchor="w", pady=(0, 5))
staff_id_entry = ttk.Entry(staff_container, font=("Helvetica", 11))
staff_id_entry.pack(fill="x", pady=(0, 15))

tk.Label(
    staff_container,
    text="Select Court Number",
    font=("Helvetica", 11, "bold"),
    bg=IITH_CARD,
    fg=IITH_NAVY,
).pack(anchor="w", pady=(0, 5))

court_combo = ttk.Combobox(
    staff_container,
    values=[1, 2, 3, 4],
    state="readonly",
    font=("Helvetica", 11),
)
court_combo.set(1)
court_combo.pack(fill="x", pady=(0, 15))

tk.Label(
    staff_container,
    text="Update Availability Status",
    font=("Helvetica", 11, "bold"),
    bg=IITH_CARD,
    fg=IITH_NAVY,
).pack(anchor="w", pady=(0, 5))

status_combo = ttk.Combobox(
    staff_container,
    values=[
        "EMPTY",
        "FULL",
        "MAINTENANCE",
        "OFFICIAL MATCH",
        "NSO Practice",
        "Inter-IIT Practice",
    ],
    state="readonly",
    font=("Helvetica", 11),
)
status_combo.set("FULL")
status_combo.pack(fill="x", pady=(0, 20))


def update_court_status():
    staff_id = staff_id_entry.get().strip()
    court = court_combo.get()
    status = status_combo.get()

    if not staff_id.isdigit():
        messagebox.showwarning(
            "Input Error", "Please enter a valid numeric Staff ID."
        )
        return

    try:
        con = get_db_connection()
        cur = con.cursor()

        cur.execute("SELECT id FROM staff WHERE id = ?", (int(staff_id),))
        if cur.fetchone():
            cur.execute(
                "UPDATE badminton SET availability = ? WHERE Court_No = ?",
                (status, court),
            )
            con.commit()
            messagebox.showinfo(
                "Success", f"Court {court} set to '{status}'!"
            )
            fetch_courts_and_queue()
        else:
            messagebox.showerror("Access Denied", "Invalid Staff ID!")

        con.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Update failed:\n{e}")


ttk.Button(
    staff_container,
    text="Submit Status Update",
    style="Primary.TButton",
    command=update_court_status,
).pack(fill="x", pady=(0, 12))


def admit_next_in_queue():
    staff_id = staff_id_entry.get().strip()
    court = court_combo.get()

    if not staff_id.isdigit():
        messagebox.showwarning(
            "Input Error", "Please enter a valid numeric Staff ID."
        )
        return

    try:
        con = get_db_connection()
        cur = con.cursor()

        cur.execute("SELECT id FROM staff WHERE id = ?", (int(staff_id),))
        if cur.fetchone():
            cur.execute(
                "SELECT queue_id, student_name, roll_no FROM court_queue WHERE"
                " court_no = ? ORDER BY queue_id ASC LIMIT 1",
                (court,),
            )
            next_student = cur.fetchone()

            if next_student:
                q_id, s_name, r_no = next_student
                cur.execute(
                    "DELETE FROM court_queue WHERE queue_id = ?", (q_id,)
                )
                cur.execute(
                    "UPDATE badminton SET availability = 'FULL' WHERE Court_No"
                    " = ?",
                    (court,),
                )
                con.commit()

                messagebox.showinfo(
                    "Court Assigned",
                    f"Court {court} assigned to next student in line:\n\nName:"
                    f" {s_name}\nRoll No: {r_no}",
                )
                fetch_courts_and_queue()
            else:
                messagebox.showinfo(
                    "Queue Empty",
                    f"No students currently waiting for Court {court}.",
                )
        else:
            messagebox.showerror("Access Denied", "Invalid Staff ID!")

        con.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Action failed:\n{e}")


ttk.Button(
    staff_container,
    text="▶ Admit Next Student in Queue",
    style="Secondary.TButton",
    command=admit_next_in_queue,
).pack(fill="x")

fetch_courts_and_queue()
root.mainloop()