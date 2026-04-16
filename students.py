import tkinter as tk
from tkinter import ttk, messagebox
from data import (
    load_students as db_load_students,
    add_student as db_add_student,
    update_student as db_update_student,
    delete_student as db_delete_student,
)


BG = "#0f172a"
CARD = "#111827"
CARD_2 = "#1e293b"
ACCENT = "#38bdf8"
ACCENT_2 = "#818cf8"
TEXT = "#f8fafc"
MUTED = "#94a3b8"
ENTRY_BG = "#0b1220"
SUCCESS = "#22c55e"
WARNING = "#f59e0b"
DANGER = "#ef4444"


def main():
    students = db_load_students()

    root = tk.Tk()
    root.title("Student Management System")
    root.geometry("1280x720")
    root.minsize(1150, 650)
    root.configure(bg=BG)

    # -------------------- STYLE --------------------
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background="#0b1220",
        foreground=TEXT,
        fieldbackground="#0b1220",
        rowheight=34,
        font=("Segoe UI", 10),
        borderwidth=0,
    )

    style.configure(
        "Treeview.Heading",
        background=ACCENT_2,
        foreground="white",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
    )

    style.map(
        "Treeview",
        background=[("selected", "#1d4ed8")],
        foreground=[("selected", "white")]
    )

    # -------------------- HELPERS --------------------
    def create_label(parent, text, size=11, bold=False, fg=TEXT, bg=CARD):
        return tk.Label(
            parent,
            text=text,
            font=("Segoe UI", size, "bold" if bold else "normal"),
            fg=fg,
            bg=bg,
        )

    def create_entry(parent, width=24):
        entry = tk.Entry(
            parent,
            font=("Segoe UI", 11),
            bg=ENTRY_BG,
            fg=TEXT,
            insertbackground="white",
            relief="flat",
            width=width,
        )
        return entry

    def create_button(parent, text, command, bg, hover, fg="white", width=16):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg=bg,
            fg=fg,
            activebackground=hover,
            activeforeground=fg,
            relief="flat",
            bd=0,
            cursor="hand2",
            width=width,
            pady=10,
        )

        def on_enter(e):
            btn.config(bg=hover)

        def on_leave(e):
            btn.config(bg=bg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def create_stat_card(parent, title, value, side="left"):
        card = tk.Frame(parent, bg=CARD_2, bd=0, highlightthickness=1, highlightbackground="#243041")
        card.pack(side=side, fill="both", expand=True, padx=8, pady=5)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 11),
            bg=CARD_2,
            fg=MUTED
        ).pack(anchor="w", padx=18, pady=(14, 4))

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 22, "bold"),
            bg=CARD_2,
            fg=TEXT
        )
        value_label.pack(anchor="w", padx=18, pady=(0, 14))
        return value_label

    # -------------------- HEADER --------------------
    header = tk.Frame(root, bg=BG)
    header.pack(fill="x", padx=20, pady=(18, 10))

    title_block = tk.Frame(header, bg=BG)
    title_block.pack(side="left")

    tk.Label(
        title_block,
        text="Student Management Dashboard",
        font=("Segoe UI", 26, "bold"),
        bg=BG,
        fg=TEXT,
    ).pack(anchor="w")

    tk.Label(
        title_block,
        text="A modern and attractive student record manager",
        font=("Segoe UI", 11),
        bg=BG,
        fg=MUTED,
    ).pack(anchor="w", pady=(4, 0))

    glow = tk.Frame(header, bg=ACCENT, height=4, width=220)
    glow.pack(side="right", padx=5, pady=15)

    # -------------------- STATS --------------------
    stats_frame = tk.Frame(root, bg=BG)
    stats_frame.pack(fill="x", padx=20, pady=(0, 12))

    total_label = create_stat_card(stats_frame, "Total Students", "0")
    selected_label = create_stat_card(stats_frame, "Selected Student", "None")
    search_label = create_stat_card(stats_frame, "Search Status", "All Records")

    # -------------------- MAIN LAYOUT --------------------
    body = tk.Frame(root, bg=BG)
    body.pack(fill="both", expand=True, padx=20, pady=(0, 18))

    # LEFT PANEL
    left_panel = tk.Frame(body, bg=CARD, highlightthickness=1, highlightbackground="#243041")
    left_panel.pack(side="left", fill="y", padx=(0, 14))

    create_label(left_panel, "Student Form", size=17, bold=True).grid(
        row=0, column=0, columnspan=2, sticky="w", padx=22, pady=(20, 16)
    )

    fields = [
        ("Student ID", 1),
        ("Full Name", 2),
        ("Age", 3),
        ("Course", 4),
        ("Search", 5),
    ]

    entries = {}
    for text, row in fields:
        create_label(left_panel, text, size=10, bold=True, fg=MUTED).grid(
            row=row, column=0, sticky="w", padx=22, pady=8
        )
        entry = create_entry(left_panel, width=28)
        entry.grid(row=row, column=1, padx=22, pady=8, ipady=8)
        entries[text] = entry

    e_id = entries["Student ID"]
    e_name = entries["Full Name"]
    e_age = entries["Age"]
    e_course = entries["Course"]
    e_search = entries["Search"]

    button_frame = tk.Frame(left_panel, bg=CARD)
    button_frame.grid(row=6, column=0, columnspan=2, padx=16, pady=20)

    # RIGHT PANEL
    right_panel = tk.Frame(body, bg=CARD, highlightthickness=1, highlightbackground="#243041")
    right_panel.pack(side="right", fill="both", expand=True)

    top_bar = tk.Frame(right_panel, bg=CARD)
    top_bar.pack(fill="x", padx=20, pady=(20, 8))

    create_label(top_bar, "Student Records", size=17, bold=True).pack(side="left")
    create_label(top_bar, "Click a row to edit", size=10, fg=MUTED).pack(side="right")

    table_container = tk.Frame(right_panel, bg=CARD)
    table_container.pack(fill="both", expand=True, padx=20, pady=(5, 20))

    columns = ("ID", "Name", "Age", "Course")
    tree = ttk.Treeview(table_container, columns=columns, show="headings")

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Course", text="Course")

    tree.column("ID", width=130, anchor="center")
    tree.column("Name", width=300, anchor="w")
    tree.column("Age", width=100, anchor="center")
    tree.column("Course", width=240, anchor="w")

    scrollbar_y = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
    scrollbar_x = ttk.Scrollbar(table_container, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    table_container.rowconfigure(0, weight=1)
    table_container.columnconfigure(0, weight=1)

    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    # striped rows
    tree.tag_configure("odd", background="#0f1a2b")
    tree.tag_configure("even", background="#111827")

    # -------------------- FUNCTIONS --------------------
    def clear_fields():
        e_id.delete(0, tk.END)
        e_name.delete(0, tk.END)
        e_age.delete(0, tk.END)
        e_course.delete(0, tk.END)
        e_search.delete(0, tk.END)
        tree.selection_remove(tree.selection())
        selected_label.config(text="None")
        search_label.config(text="All Records")

    def refresh_list(data=None):
        nonlocal students
        students = db_load_students()

        for item in tree.get_children():
            tree.delete(item)

        display_data = data if data is not None else students

        for i, s in enumerate(display_data):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert(
                "",
                tk.END,
                values=(s["id"], s["name"], s["age"], s["course"]),
                tags=(tag,)
            )

        total_label.config(text=str(len(display_data)))

    def search_student():
        keyword = e_search.get().strip().lower()

        if not keyword:
            refresh_list()
            search_label.config(text="All Records")
            return

        filtered = []
        for s in students:
            sid = str(s.get("id", "")).lower()
            name = str(s.get("name", "")).lower()
            age = str(s.get("age", "")).lower()
            course = str(s.get("course", "")).lower()

            if keyword in sid or keyword in name or keyword in age or keyword in course:
                filtered.append(s)

        refresh_list(filtered)

        if filtered:
            search_label.config(text=f"{len(filtered)} Found")
        else:
            search_label.config(text="No Match")
            messagebox.showinfo("Search", "No matching student found.")

    def add_student_ui():
        sid = e_id.get().strip()
        name = e_name.get().strip()
        age = e_age.get().strip()
        course = e_course.get().strip()

        if not sid or not name:
            messagebox.showwarning("Warning", "ID and Name are required.")
            return

        if any(str(s["id"]) == sid for s in students):
            messagebox.showwarning("Warning", f"ID '{sid}' already exists.")
            return

        try:
            age_int = int(age) if age else 0
        except ValueError:
            messagebox.showwarning("Warning", "Age must be a number.")
            return

        try:
            db_add_student(sid, name, age_int, course)
            refresh_list()
            clear_fields()
            messagebox.showinfo("Success", "Student added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not add student:\n{e}")

    def update_student_ui():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a student first.")
            return

        sid = e_id.get().strip()
        name = e_name.get().strip()
        age = e_age.get().strip()
        course = e_course.get().strip()

        if not sid or not name:
            messagebox.showwarning("Warning", "ID and Name are required.")
            return

        try:
            age_int = int(age) if age else 0
        except ValueError:
            messagebox.showwarning("Warning", "Age must be a number.")
            return

        item = tree.item(sel[0])
        original_id = item["values"][0]

        if str(sid) != str(original_id):
            messagebox.showwarning("Warning", "ID cannot be changed while updating.")
            return

        try:
            db_update_student(original_id, name, age_int, course)
            refresh_list()
            clear_fields()
            messagebox.showinfo("Success", "Student updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not update student:\n{e}")

    def delete_student_ui():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a student first.")
            return

        item = tree.item(sel[0])
        sid = item["values"][0]

        if messagebox.askyesno("Confirm Delete", f"Do you want to delete student ID '{sid}'?"):
            try:
                db_delete_student(sid)
                refresh_list()
                clear_fields()
                messagebox.showinfo("Success", "Student deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete student:\n{e}")

    def on_select(event):
        sel = tree.selection()
        if sel:
            vals = tree.item(sel[0])["values"]

            e_id.delete(0, tk.END)
            e_name.delete(0, tk.END)
            e_age.delete(0, tk.END)
            e_course.delete(0, tk.END)

            e_id.insert(0, vals[0])
            e_name.insert(0, vals[1])
            e_age.insert(0, vals[2])
            e_course.insert(0, vals[3])

            selected_label.config(text=str(vals[1]))

    tree.bind("<<TreeviewSelect>>", on_select)
    e_search.bind("<Return>", lambda event: search_student())

    # -------------------- BUTTONS --------------------
    btn_add = create_button(button_frame, "Add Student", add_student_ui, SUCCESS, "#16a34a")
    btn_update = create_button(button_frame, "Update Student", update_student_ui, ACCENT_2, "#6366f1")
    btn_delete = create_button(button_frame, "Delete Student", delete_student_ui, DANGER, "#dc2626")
    btn_search = create_button(button_frame, "Search", search_student, ACCENT, "#0ea5e9", fg="#0f172a")
    btn_clear = create_button(button_frame, "Clear Fields", clear_fields, "#334155", "#475569")

    btn_add.grid(row=0, column=0, padx=8, pady=8)
    btn_update.grid(row=0, column=1, padx=8, pady=8)
    btn_delete.grid(row=1, column=0, padx=8, pady=8)
    btn_search.grid(row=1, column=1, padx=8, pady=8)
    btn_clear.grid(row=2, column=0, columnspan=2, padx=8, pady=10)

    refresh_list()
    root.mainloop()


if __name__ == "__main__":
    main()