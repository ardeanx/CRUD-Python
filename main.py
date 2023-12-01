import sqlite3
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, END, messagebox

class CRUDApp:
    def __init__(self, master):
        self.master = master
        master.title("CRUD App")

        # Database setup
        self.conn = sqlite3.connect('crud_gui_example.db')
        self.cursor = self.conn.cursor()

        # Create the 'users' table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER
            )
        ''')
        self.conn.commit()
        # GUI components
        self.label_name = Label(master, text="Name:")
        self.entry_name = Entry(master)

        self.label_age = Label(master, text="Age:")
        self.entry_age = Entry(master)

        self.btn_create = Button(master, text="Create", command=self.create_user)
        self.btn_read = Button(master, text="Read", command=self.read_users)
        self.btn_update = Button(master, text="Update", command=self.update_user)
        self.btn_delete = Button(master, text="Delete", command=self.delete_user)

        self.user_listbox = Listbox(master, selectmode="SINGLE", exportselection=False)
        self.scrollbar = Scrollbar(master, orient="vertical", command=self.user_listbox.yview)
        self.user_listbox.config(yscrollcommand=self.scrollbar.set)

        # Place GUI components
        self.label_name.grid(row=0, column=0, sticky="e")
        self.entry_name.grid(row=0, column=1)

        self.label_age.grid(row=1, column=0, sticky="e")
        self.entry_age.grid(row=1, column=1)

        self.btn_create.grid(row=2, column=0, columnspan=2, pady=10)
        self.btn_read.grid(row=3, column=0, columnspan=2, pady=5)
        self.btn_update.grid(row=4, column=0, columnspan=2, pady=5)
        self.btn_delete.grid(row=5, column=0, columnspan=2, pady=5)

        self.user_listbox.grid(row=0, column=2, rowspan=6, padx=10, pady=10, sticky="nsew")
        self.scrollbar.grid(row=0, column=3, rowspan=6, sticky="ns")

        # Set grid weights for resizing
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(2, weight=1)

    def create_user(self):
        name = self.entry_name.get()
        age = self.entry_age.get()
        if name and age:
            self.cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
            self.conn.commit()
            messagebox.showinfo("Success", "User created successfully.")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Please enter both name and age.")

    def read_users(self):
        self.user_listbox.delete(0, END)
        self.cursor.execute('SELECT * FROM users')
        users = self.cursor.fetchall()
        for user in users:
            self.user_listbox.insert(END, f"{user[0]} - {user[1]} ({user[2]} years old)")

    def update_user(self):
        selected_user = self.user_listbox.curselection()
        if selected_user:
            user_id = selected_user[0] + 1
            new_name = self.entry_name.get()
            new_age = self.entry_age.get()
            if new_name and new_age:
                self.cursor.execute('UPDATE users SET name=?, age=? WHERE id=?', (new_name, new_age, user_id))
                self.conn.commit()
                messagebox.showinfo("Success", "User updated successfully.")
                self.clear_entries()
                self.read_users()
            else:
                messagebox.showerror("Error", "Please enter both name and age.")
        else:
            messagebox.showerror("Error", "Please select a user to update.")

    def delete_user(self):
        selected_user = self.user_listbox.curselection()
        if selected_user:
            user_id = selected_user[0] + 1
            self.cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "User deleted successfully.")
            self.read_users()
        else:
            messagebox.showerror("Error", "Please select a user to delete.")

    def clear_entries(self):
        self.entry_name.delete(0, END)
        self.entry_age.delete(0, END)

# Run the Tkinter application
if __name__ == "__main__":
    root = Tk()
    app = CRUDApp(root)
    root.mainloop()

# Close the database connection when the GUI is closed
app.conn.close()
