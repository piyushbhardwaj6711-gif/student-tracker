import tkinter as tk
from tkinter import ttk, messagebox
from data import (
    load_students as db_load_students,
    add_student as db_add_student,
    update_student as db_update_student,
    delete_student as db_delete_student,
)

# ==================== COLORS ====================
BG = "#0b1120"
SIDEBAR = "#111827"
PANEL = "#0f172a"
CARD = "#131c31"
CARD_2 = "#1b2640"
INPUT_BG = "#0b1220"
INPUT_BORDER = "#334155"

PRIMARY = "#6366f1"
PRIMARY_HOVER = "#4f46e5"
CYAN = "#06b6d4"
CYAN_HOVER = "#0891b2"
SUCCESS = "#22c55e"
SUCCESS_HOVER = "#16a34a"
DANGER = "#ef4444"
DANGER_HOVER = "#dc2626"
WARNING = "#f59e0b"
WARNING_HOVER = "#d97706"
GRAY_BTN = "#334155"
GRAY_BTN_HOVER = "#475569"

TEXT = "#f8fafc"
MUTED = "#94a3b8"
LIGHT = "#cbd5e1"

FONT = "Segoe UI"


def main():
    students = db_load_students()

    root = tk.Tk()
    root.title("Student Tracker Pro")
    root.geometry("1360x780")
    root.minsize(1200, 700)
    root.configure(bg=BG)

    # ==================== STYLE ====================
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        background=INPUT_BG,
        foreground=TEXT,
        fieldbackground=INPUT_BG,
        borderwidth=0,
        relief="flat",
        rowheight=38,
        font=(FONT, 10),
    )

    style.configure(
        "Treeview.Heading",
        background=PRIMARY,
        foreground="white",
        relief="flat",
        borderwidth=0,
        font=(FONT, 11, "bold"),
        padding=8,
    )

    style.map(
        "Treeview",
        background=[("selected", "#1d4ed8")],
        foreground=[("selected", "white")]
    )

    style.configure(
        "Vertical.TScrollbar",
        background=CARD_2,
        troughcolor=PANEL,
        bordercolor=PANEL,
        arrowcolor=TEXT,
    )

    style.configure(
        "Horizontal.TScrollbar",
        background=CARD_2,
        troughcolor=PANEL,
        bordercolor=PANEL,
        arrowcolor=TEXT,
    )

    # ==================== HELPERS ====================
    def rounded_panel(parent, bg_color, **pack_kwargs):
        frame = tk.Frame(
            parent,
            bg=bg_color,
            highlightthickness=1,
            highlightbackground="#22304a",
            bd=0
        )
        if pack_kwargs:
            frame.pack(**pack_kwargs)
        return frame

    def make_label(parent, text, size=11, bold=False, fg=TEXT, bg=None):
        return tk.Label(
            parent,
            text=text,
            font=(FONT, size, "bold" if bold else "normal"),
            fg=fg,
            bg=bg if bg else parent.cget("bg")
        )

    def create_entry(parent, width=28):
        outer = tk.Frame(parent, bg=INPUT_BORDER, bd=0, highlightthickness=0)
        entry = tk.Entry(
            outer,
            font=(FONT, 11),
            bg=INPUT_BG,
            fg=TEXT,
            insertbackground="white",
            relief="flat",
            bd=0,
            width=width,
        )
        entry.pack(fill="both", expand=True, padx=1, pady=1, ipady=10)

        def on_focus_in(event):
            outer.config(bg=PRIMARY)

        def on_focus_out(event):
            outer.config(bg=INPUT_BORDER)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        return outer, entry

    def create_button(parent, text, command, bg, hover, fg="white", width=15):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=(FONT, 10, "bold"),
            bg=bg,
            fg=fg,
            activebackground=hover,
            activeforeground=fg,
            relief="flat",
            bd=0,
            cursor="hand2",
            width=width,
            pady=11,
        )

        def on_enter(e):
            btn.config(bg=hover)

        def on_leave(e):
            btn.config(bg=bg)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def create_stat_card(parent, title, value, subtitle, color):
        card = tk.Frame(
            parent,
            bg=CARD,
            highlightthickness=1,
            highlightbackground="#22304a",
            bd=0
        )
        card.pack(side="left", fill="both", expand=True, padx=8)

        top = tk.Frame(card, bg=CARD)
        top.pack(fill="x", padx=18, pady=(16, 8))

        dot = tk.Canvas(top, width=14, height=14, bg=CARD, highlightthickness=0)
        dot.create_oval(2, 2, 12, 12, fill=color, outline=color)
        dot.pack(side="left", padx=(0, 8))

        tk.Label(
            top,
            text=title,
            font=(FONT, 10, "bold"),
            fg=LIGHT,
            bg=CARD
        ).pack(side="left")

        value_label = tk.Label(
            card,
            text=value,
            font=(FONT, 24, "bold"),
            fg=TEXT,
            bg=CARD
        )
        value_label.pack(anchor="w", padx=18)

        sub_label = tk.Label(
            card,
            text=subtitle,
            font=(FONT, 9),
            fg=MUTED,
            bg=CARD
        )
        sub_label.pack(anchor="w", padx=18, pady=(4, 16))

        return value_label, sub_label

    def clear_entry(widget):
        widget.delete(0, tk.END)

    # ==================== LAYOUT ====================
    main_wrap = tk.Frame(root, bg=BG)
    main_wrap.pack(fill="both", expand=True, padx=18, pady=18)

    # ---------- SIDEBAR ----------
    sidebar = tk.Frame(
        main_wrap,
        bg=SIDEBAR,
        width=270,
        highlightthickness=1,
        highlightbackground="#22304a"
    )
    sidebar.pack(side="left", fill="y", padx=(0, 14))
    sidebar.pack_propagate(False)

    logo_box = tk.Frame(sidebar, bg=SIDEBAR)
    logo_box.pack(fill="x", padx=22, pady=(24, 10))

    tk.Label(
        logo_box,
        text="ST",
        font=(FONT, 22, "bold"),
        fg="white",
        bg=PRIMARY,
        width=3,
        height=1
    ).pack(anchor="w")

    tk.Label(
        logo_box,
        text="Student Tracker",
        font=(FONT, 18, "bold"),
        fg=TEXT,
        bg=SIDEBAR
    ).pack(anchor="w", pady=(14, 2))

    tk.Label(
        logo_box,
        text="Manage student records ",
        font=(FONT, 10),
        fg=MUTED,
        bg=SIDEBAR,
        wraplength=210,
        justify="left"
    ).pack(anchor="w")

    quick_panel = tk.Frame(sidebar, bg=SIDEBAR)
    quick_panel.pack(fill="x", padx=22, pady=(20, 16))

    tk.Label(
        quick_panel,
        text="Quick Tips",
        font=(FONT, 11, "bold"),
        fg=TEXT,
        bg=SIDEBAR
    ).pack(anchor="w", pady=(0, 10))

    tips = [
        "• Click any row to edit student details",
        "• Press Enter in search box to search",
        "• Student ID cannot be changed while updating",
        "• Clear fields before adding a new student",
    ]

    for tip in tips:
        tk.Label(
            quick_panel,
            text=tip,
            font=(FONT, 9),
            fg=MUTED,
            bg=SIDEBAR,
            wraplength=210,
            justify="left"
        ).pack(anchor="w", pady=5)

    # ---------- CONTENT ----------
    content = tk.Frame(main_wrap, bg=BG)
    content.pack(side="left", fill="both", expand=True)

    # ==================== HEADER ====================
    header = tk.Frame(content, bg=BG)
    header.pack(fill="x", pady=(0, 14))

    left_header = tk.Frame(header, bg=BG)
    left_header.pack(side="left")

    tk.Label(
        left_header,
        text="Student Management Dashboard",
        font=(FONT, 28, "bold"),
        fg=TEXT,
        bg=BG
    ).pack(anchor="w")

    tk.Label(
        left_header,
        text="student tracker",
        font=(FONT, 11),
        fg=MUTED,
        bg=BG
    ).pack(anchor="w", pady=(5, 0))

    right_header = tk.Frame(header, bg=BG)
    right_header.pack(side="right")

    status_badge = tk.Label(
        right_header,
        text="● Live Records",
        font=(FONT, 10, "bold"),
        fg="#86efac",
        bg=CARD,
        padx=16,
        pady=10
    )
    status_badge.pack()

    # ==================== STATS ====================
    stats_frame = tk.Frame(content, bg=BG)
    stats_frame.pack(fill="x", pady=(0, 14))

    total_label, total_sub = create_stat_card(stats_frame, "Total Students", "0", "Records in database", PRIMARY)
    selected_label, selected_sub = create_stat_card(stats_frame, "Selected Student", "None", "Current active row", CYAN)
    search_label, search_sub = create_stat_card(stats_frame, "Search Status", "All Records", "Current table filter", SUCCESS)

    # ==================== BODY ====================
    body = tk.Frame(content, bg=BG)
    body.pack(fill="both", expand=True)

    # ---------- FORM PANEL ----------
    form_panel = rounded_panel(body, PANEL)
    form_panel.pack(side="left", fill="y", padx=(0, 14))
    form_panel.config(width=360)
    form_panel.pack_propagate(False)

    # Keep form usable on smaller screens by scrolling only fields.
    # Action buttons stay fixed at the bottom so they are always visible.
    form_body = tk.Frame(form_panel, bg=PANEL)
    form_body.pack(side="top", fill="both", expand=True)

    form_canvas = tk.Canvas(form_body, bg=PANEL, highlightthickness=0, bd=0)
    form_scrollbar = ttk.Scrollbar(form_body, orient="vertical", command=form_canvas.yview, style="Vertical.TScrollbar")
    form_canvas.configure(yscrollcommand=form_scrollbar.set)

    form_canvas.pack(side="left", fill="both", expand=True)
    form_scrollbar.pack(side="right", fill="y")

    form_content = tk.Frame(form_canvas, bg=PANEL)
    form_window = form_canvas.create_window((0, 0), window=form_content, anchor="nw")

    def _sync_form_scroll_region(event=None):
        form_canvas.configure(scrollregion=form_canvas.bbox("all"))

    def _sync_form_width(event):
        form_canvas.itemconfigure(form_window, width=event.width)

    form_content.bind("<Configure>", _sync_form_scroll_region)
    form_canvas.bind("<Configure>", _sync_form_width)

    form_head = tk.Frame(form_content, bg=PANEL)
    form_head.pack(fill="x", padx=22, pady=(22, 14))

    tk.Label(
        form_head,
        text="Student Form",
        font=(FONT, 18, "bold"),
        fg=TEXT,
        bg=PANEL
    ).pack(anchor="w")

    tk.Label(
        form_head,
        text="Add, update or delete student details",
        font=(FONT, 10),
        fg=MUTED,
        bg=PANEL
    ).pack(anchor="w", pady=(4, 0))

    form_fields = tk.Frame(form_content, bg=PANEL)
    form_fields.pack(fill="x", padx=22, pady=(6, 10))

    entries = {}

    field_names = ["Student ID", "Full Name", "Age", "Course", "Search"]

    for field in field_names:
        make_label(form_fields, field, size=10, bold=True, fg=LIGHT, bg=PANEL).pack(anchor="w", pady=(10, 6))
        wrapper, entry = create_entry(form_fields, width=28)
        wrapper.pack(fill="x")
        entries[field] = entry

    e_id = entries["Student ID"]
    e_name = entries["Full Name"]
    e_age = entries["Age"]
    e_course = entries["Course"]
    e_search = entries["Search"]

    button_frame = tk.Frame(form_panel, bg=PANEL)
    button_frame.pack(side="bottom", fill="x", padx=22, pady=(12, 18))

    btn_add = create_button(button_frame, "Add Student", lambda: add_student_ui(), SUCCESS, SUCCESS_HOVER)
    btn_update = create_button(button_frame, "Update Student", lambda: update_student_ui(), PRIMARY, PRIMARY_HOVER)
    btn_delete = create_button(button_frame, "Delete Student", lambda: delete_student_ui(), DANGER, DANGER_HOVER)
    btn_search = create_button(button_frame, "Search", lambda: search_student(), CYAN, CYAN_HOVER, fg="#0b1120")
    btn_clear = create_button(button_frame, "Clear Fields", lambda: clear_fields(), GRAY_BTN, GRAY_BTN_HOVER)

    btn_add.grid(row=0, column=0, padx=6, pady=6)
    btn_update.grid(row=0, column=1, padx=6, pady=6)
    btn_delete.grid(row=1, column=0, padx=6, pady=6)
    btn_search.grid(row=1, column=1, padx=6, pady=6)
    btn_clear.grid(row=2, column=0, columnspan=2, padx=6, pady=(10, 6), sticky="ew")

    # ---------- TABLE PANEL ----------
    table_panel = rounded_panel(body, PANEL)
    table_panel.pack(side="right", fill="both", expand=True)

    table_top = tk.Frame(table_panel, bg=PANEL)
    table_top.pack(fill="x", padx=20, pady=(20, 8))

    tk.Label(
        table_top,
        text="Student Records",
        font=(FONT, 18, "bold"),
        fg=TEXT,
        bg=PANEL
    ).pack(side="left")

    tk.Label(
        table_top,
        text="Select a row to auto-fill the form",
        font=(FONT, 10),
        fg=MUTED,
        bg=PANEL
    ).pack(side="right")

    line = tk.Frame(table_panel, bg="#22304a", height=1)
    line.pack(fill="x", padx=20, pady=(0, 10))

    table_container = tk.Frame(table_panel, bg=PANEL)
    table_container.pack(fill="both", expand=True, padx=20, pady=(4, 20))

    columns = ("ID", "Name", "Age", "Course")
    tree = ttk.Treeview(table_container, columns=columns, show="headings")

    tree.heading("ID", text="Student ID")
    tree.heading("Name", text="Full Name")
    tree.heading("Age", text="Age")
    tree.heading("Course", text="Course")

    tree.column("ID", width=130, anchor="center")
    tree.column("Name", width=320, anchor="w")
    tree.column("Age", width=100, anchor="center")
    tree.column("Course", width=240, anchor="w")

    scrollbar_y = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview, style="Vertical.TScrollbar")
    scrollbar_x = ttk.Scrollbar(table_container, orient="horizontal", command=tree.xview, style="Horizontal.TScrollbar")

    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    table_container.rowconfigure(0, weight=1)
    table_container.columnconfigure(0, weight=1)

    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    tree.tag_configure("odd", background="#0f172a")
    tree.tag_configure("even", background="#111c33")

    # ---------- FOOTER STATUS ----------
    footer = tk.Frame(content, bg=BG)
    footer.pack(fill="x", pady=(12, 0))

    footer_status = tk.Label(
        footer,
        text="Ready",
        font=(FONT, 10),
        fg=MUTED,
        bg=BG
    )
    footer_status.pack(anchor="w")

    # ==================== FUNCTIONS ====================
    def set_status(text, color=MUTED):
        footer_status.config(text=text, fg=color)

    def clear_fields():
        clear_entry(e_id)
        clear_entry(e_name)
        clear_entry(e_age)
        clear_entry(e_course)
        clear_entry(e_search)
        tree.selection_remove(tree.selection())
        selected_label.config(text="None")
        selected_sub.config(text="Current active row")
        search_label.config(text="All Records")
        search_sub.config(text="Current table filter")
        set_status("Fields cleared", LIGHT)

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

        if data is None:
            total_sub.config(text="Records in database")
        else:
            total_sub.config(text="Visible results in table")

        set_status(f"{len(display_data)} record(s) loaded", LIGHT)

    def search_student():
        keyword = e_search.get().strip().lower()

        if not keyword:
            refresh_list()
            search_label.config(text="All Records")
            search_sub.config(text="Showing complete student list")
            set_status("Showing all records", CYAN)
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
            search_sub.config(text=f"Matched keyword: {keyword}")
            set_status(f"Found {len(filtered)} matching student(s)", SUCCESS)
        else:
            search_label.config(text="No Match")
            search_sub.config(text=f"No result for: {keyword}")
            set_status("No matching student found", WARNING)
            messagebox.showinfo("Search", "No matching student found.")

    def add_student_ui():
        sid = e_id.get().strip()
        name = e_name.get().strip()
        age = e_age.get().strip()
        course = e_course.get().strip()

        if not sid or not name:
            set_status("ID and Name are required", DANGER)
            messagebox.showwarning("Warning", "ID and Name are required.")
            return

        if any(str(s["id"]) == sid for s in students):
            set_status(f"ID '{sid}' already exists", DANGER)
            messagebox.showwarning("Warning", f"ID '{sid}' already exists.")
            return

        try:
            age_int = int(age) if age else 0
        except ValueError:
            set_status("Age must be numeric", DANGER)
            messagebox.showwarning("Warning", "Age must be a number.")
            return

        try:
            db_add_student(sid, name, age_int, course)
            refresh_list()
            clear_fields()
            set_status("Student added successfully", SUCCESS)
            messagebox.showinfo("Success", "Student added successfully.")
        except Exception as e:
            set_status("Could not add student", DANGER)
            messagebox.showerror("Error", f"Could not add student:\n{e}")

    def update_student_ui():
        sel = tree.selection()
        if not sel:
            set_status("Select a student first", WARNING)
            messagebox.showwarning("Warning", "Select a student first.")
            return

        sid = e_id.get().strip()
        name = e_name.get().strip()
        age = e_age.get().strip()
        course = e_course.get().strip()

        if not sid or not name:
            set_status("ID and Name are required", DANGER)
            messagebox.showwarning("Warning", "ID and Name are required.")
            return

        try:
            age_int = int(age) if age else 0
        except ValueError:
            set_status("Age must be numeric", DANGER)
            messagebox.showwarning("Warning", "Age must be a number.")
            return

        item = tree.item(sel[0])
        original_id = item["values"][0]

        if str(sid) != str(original_id):
            set_status("ID cannot be changed while updating", WARNING)
            messagebox.showwarning("Warning", "ID cannot be changed while updating.")
            return

        try:
            db_update_student(original_id, name, age_int, course)
            refresh_list()
            clear_fields()
            set_status("Student updated successfully", SUCCESS)
            messagebox.showinfo("Success", "Student updated successfully.")
        except Exception as e:
            set_status("Could not update student", DANGER)
            messagebox.showerror("Error", f"Could not update student:\n{e}")

    def delete_student_ui():
        sel = tree.selection()
        if not sel:
            set_status("Select a student first", WARNING)
            messagebox.showwarning("Warning", "Select a student first.")
            return

        item = tree.item(sel[0])
        sid = item["values"][0]

        if messagebox.askyesno("Confirm Delete", f"Do you want to delete student ID '{sid}'?"):
            try:
                db_delete_student(sid)
                refresh_list()
                clear_fields()
                set_status("Student deleted successfully", SUCCESS)
                messagebox.showinfo("Success", "Student deleted successfully.")
            except Exception as e:
                set_status("Could not delete student", DANGER)
                messagebox.showerror("Error", f"Could not delete student:\n{e}")

    def on_select(event):
        sel = tree.selection()
        if sel:
            vals = tree.item(sel[0])["values"]

            clear_entry(e_id)
            clear_entry(e_name)
            clear_entry(e_age)
            clear_entry(e_course)

            e_id.insert(0, vals[0])
            e_name.insert(0, vals[1])
            e_age.insert(0, vals[2])
            e_course.insert(0, vals[3])

            selected_label.config(text=str(vals[1]))
            selected_sub.config(text=f"Student ID: {vals[0]}")
            set_status(f"Selected: {vals[1]}", CYAN)

    tree.bind("<<TreeviewSelect>>", on_select)
    e_search.bind("<Return>", lambda event: search_student())

    refresh_list()
    root.mainloop()


if __name__ == "__main__":
    main()