import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "students.json"


def load_students():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_students(students):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(students, f, indent=2)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Could not save: {e}")
        return False


def main():
    students = load_students()

    root = tk.Tk()
    root.title("Student Record Manager")
    root.geometry("700x450")

    # Labels and entries
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(fill=tk.X)

    tk.Label(frame, text="ID:").grid(row=0, column=0, sticky="w", pady=2)
    tk.Label(frame, text="Name:").grid(row=1, column=0, sticky="w", pady=2)
    tk.Label(frame, text="Age:").grid(row=2, column=0, sticky="w", pady=2)
    tk.Label(frame, text="Course:").grid(row=3, column=0, sticky="w", pady=2)
    tk.Label(frame, text="Search (ID/Name):").grid(row=4, column=0, sticky="w", pady=2)


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

    def add_student():
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
        students.append({"id": sid, "name": name, "age": age_int, "course": course})
        if save_students(students):
            refresh_list()
            clear_fields()
            messagebox.showinfo("Done", "Student added.")

    def update_student():
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
        for i, s in enumerate(students):
            if s["id"] == sid:
                students[i] = {"id": sid, "name": name, "age": age_int, "course": course}
                if save_students(students):
                    refresh_list()
                    clear_fields()
                    messagebox.showinfo("Done", "Student updated.")
                return
        messagebox.showwarning("Warning", "Student not found.")

    def delete_student():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a student first.")
            return
        item = tree.item(sel[0])
        sid = item["values"][0]
        if messagebox.askyesno("Confirm", f"Delete student '{sid}'?"):
            students[:] = [s for s in students if s["id"] != sid]
            if save_students(students):
                refresh_list()
                clear_fields()
                messagebox.showinfo("Done", "Student deleted.")
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

    tk.Button(btn_frame, text="Add", command=add_student, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Update", command=update_student, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Delete", command=delete_student, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Clear", command=clear_fields, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Search", command=search_student, width=10).pack(side=tk.LEFT, padx=5)

    refresh_list()
    root.mainloop()


if __name__ == "__main__":
    main()
