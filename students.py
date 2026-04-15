import tkinter as tk
from tkinter import ttk, messagebox
from data import (
    load_students as db_load_students,
    add_student as db_add_student,
    update_student as db_update_student,
    delete_student as db_delete_student,
)


def main():
    students = db_load_students()

    root = tk.Tk()
    root.title("Student Record Manager")
    root.geometry("900x550")
    root.configure(bg="#f4f6f8")
    # Labels and entries
    title_label = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 25, "bold"),
    bg="#f4f6f8",
    fg="#222"
)
    main_frame = tk.Frame(root, bg="#f4f6f8")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    left_frame = tk.Frame(main_frame, bg="white", bd=1, relief="solid")
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

    right_frame = tk.Frame(main_frame, bg="white", bd=1, relief="solid")
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    title_label.pack(pady=10)
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(fill=tk.X)

    tk.Label(frame, text="ID:").grid(row=0, column=0, sticky="w", pady=2)
    tk.Label(frame, text="Name:").grid(row=1, column=0, sticky="w", pady=2)
    tk.Label(frame, text="Age:").grid(row=2, column=0, sticky="w", pady=2)
    tk.Label(frame, text="Course:").grid(row=3, column=0, sticky="w", pady=2)

    
    tk.Label(frame, text="Search (ID/Name):").grid(row=4, column=0, sticky="w", pady=2)
    tk.Label(left_frame, text="ID:", font=("Arial", 11), bg="white").grid(row=0, column=0, sticky="w", pady=5, padx=10)
    e_id = tk.Entry(left_frame, width=25, font=("Arial", 11))
    e_id.grid(row=0, column=1, pady=5, padx=10)

    tk.Label(left_frame, text="Name:", font=("Arial", 11), bg="white").grid(row=1, column=0, sticky="w", pady=5, padx=10)
    e_name = tk.Entry(left_frame, width=25, font=("Arial", 11))
    e_name.grid(row=1, column=1, pady=5, padx=10)

    e_id = tk.Entry(frame, width=30)
    e_name = tk.Entry(frame, width=30)
    e_age = tk.Entry(frame, width=30)
    e_course = tk.Entry(frame, width=30)
    e_search = tk.Entry(frame, width=30)


    e_id.grid(row=0, column=1, pady=2, padx=5)
    e_name.grid(row=1, column=1, pady=2, padx=5)
    e_age.grid(row=2, column=1, pady=2, padx=5)
    e_course.grid(row=3, column=1, pady=2, padx=5)
    e_search.grid(row=4, column=1, pady=2, padx=5)
    # Treeview
    columns = ("ID", "Name", "Age", "Course")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def refresh_list():
        nonlocal students
        students = db_load_students()
        for item in tree.get_children():
            tree.delete(item)
        for s in students:
            tree.insert("", tk.END, values=(s["id"], s["name"], s["age"], s["course"]))

    def clear_fields():
        e_id.delete(0, tk.END)
        e_name.delete(0, tk.END)
        e_age.delete(0, tk.END)
        e_course.delete(0, tk.END)

    def search_student():
        keyword = e_search.get().strip().lower()
        for item in tree.get_children():
            tree.delete(item)
        if not keyword:
            refresh_list()
            return
        found = False
        for s in students:
            sid = str(s.get("id", "")).lower()
            name = str(s.get("name", "")).lower()
            if keyword in sid or keyword in name:
                tree.insert("", tk.END, values=(s["id"], s["name"], s["age"], s["course"]))
                found = True
        if not found:
            messagebox.showinfo("Search", "No matching student found.")

    def add_student_ui():
        sid = e_id.get().strip()
        name = e_name.get().strip()
        age = e_age.get().strip()
        course = e_course.get().strip()
        if not sid or not name:
            messagebox.showwarning("Warning", "ID and Name are required.")
            return
        if any(s["id"] == sid for s in students):
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
            messagebox.showinfo("Done", "Student added.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not add student: {e}")

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
        if sid != original_id:
            messagebox.showwarning("Warning", "ID cannot be changed while updating.")
            return
        try:
            db_update_student(original_id, name, age_int, course)
            refresh_list()
            clear_fields()
            messagebox.showinfo("Done", "Student updated.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not update student: {e}")

    def delete_student_ui():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a student first.")
            return
        item = tree.item(sel[0])
        sid = item["values"][0]
        if messagebox.askyesno("Confirm", f"Delete student '{sid}'?"):
            try:
                db_delete_student(sid)
                refresh_list()
                clear_fields()
                messagebox.showinfo("Done", "Student deleted.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete student: {e}")
    def on_select(event):
        sel = tree.selection()
        if sel:
            vals = tree.item(sel[0])["values"]
            clear_fields()
            e_id.insert(0, vals[0])
            e_name.insert(0, vals[1])
            e_age.insert(0, vals[2])
            e_course.insert(0, vals[3])

    tree.bind("<<TreeviewSelect>>", on_select)
    e_search.bind("<Return>", lambda event: search_student())

    # Buttons
    btn_frame = tk.Frame(root, pady=10)
    btn_frame.pack()

    tk.Button(btn_frame, text="Add", command=add_student_ui, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Update", command=update_student_ui, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Delete", command=delete_student_ui, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Clear", command=clear_fields, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Search", command=search_student, width=10).pack(side=tk.LEFT, padx=5)

    refresh_list()
    root.mainloop()


if __name__ == "__main__":
    main()
