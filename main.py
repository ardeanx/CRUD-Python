#Import Library Pendukung untuk membuat GUI disini saya pakai Tkinter
import sqlite3
from tkinter import Tk, Label, Entry, Button, ttk, Scrollbar, END, messagebox, Frame

#Buat Class variabel inisiasi awal
class CRUDApp:
    def __init__(self, master):
        self.master = master
        master.title("Python CRUD")
        master.iconbitmap("C:/Users/ardea/Documents/GitHub/CRUD Python/logo.ico")

        # Konfigurasi Database menggunakan SQLite3
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        # Membuat tabel 'users' jika tidak ada
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                phone TEXT,
                age INTEGER,
                email TEXT
            )
        ''')
        self.conn.commit()

        # Komponen GUI (Graphical User Interface)
        self.label_id = Label(master, text="ID:")
        self.entry_id = Entry(master)

        self.label_name = Label(master, text="Name:")
        self.entry_name = Entry(master)

        self.label_address = Label(master, text="Address:")
        self.entry_address = Entry(master)

        self.label_phone = Label(master, text="Phone:")
        self.entry_phone = Entry(master)

        self.label_age = Label(master, text="Age:")
        self.entry_age = Entry(master)

        self.label_email = Label(master, text="Email:")
        self.entry_email = Entry(master)

        # Letak Layout/Posisi Komponen GUI
        self.label_id.grid(row=0, column=0, sticky="e")
        self.entry_id.grid(row=0, column=1)

        self.label_name.grid(row=1, column=0, sticky="e")
        self.entry_name.grid(row=1, column=1)

        self.label_address.grid(row=2, column=0, sticky="e")
        self.entry_address.grid(row=2, column=1)

        self.label_phone.grid(row=3, column=0, sticky="e")
        self.entry_phone.grid(row=3, column=1)

        self.label_age.grid(row=4, column=0, sticky="e")
        self.entry_age.grid(row=4, column=1)

        self.label_email.grid(row=5, column=0, sticky="e")
        self.entry_email.grid(row=5, column=1)

        # Membuat Frame untuk Tombol
        button_frame = Frame(master)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)

        # Komponen GUI untuk tombol
        self.btn_create = Button(button_frame, text="Create", command=self.create_user)
        self.btn_read = Button(button_frame, text="Read", command=self.read_users)
        self.btn_update = Button(button_frame, text="Update", command=self.update_user)
        self.btn_delete = Button(button_frame, text="Delete", command=self.delete_user)

        # Letak Layout/Posisi Komponen Tombol
        self.btn_create.grid(row=0, column=0, padx=5)
        self.btn_read.grid(row=0, column=1, padx=5)
        self.btn_update.grid(row=0, column=2, padx=5)
        self.btn_delete.grid(row=0, column=3, padx=5)

        # Tampilan Data Tabel untuk opsi 'Read'
        self.tree = ttk.Treeview(master, columns=("ID", "Name", "Address", "Phone", "Age", "Email"), show="headings", height=7)
        self.scrollbar = Scrollbar(master, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Mendefinisikan Heading di Kolom
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Email", text="Email")

        # Letak/Layout Tabel
        self.tree.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.scrollbar.grid(row=0, column=3, sticky="ns")

        # Tetapkan grid weight untuk mengubah ukuran
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(2, weight=1)

        #Membuat entry 'create user'
    def create_user(self):
        name = self.entry_name.get()
        address = self.entry_address.get()
        phone = self.entry_phone.get()
        age = self.entry_age.get()
        email = self.entry_email.get()

        #Pengkondisian untuk mencocokan data dari database
        if name and age:
            self.cursor.execute('''
                INSERT INTO users (name, address, phone, age, email) 
                VALUES (?, ?, ?, ?, ?)
            ''', (name, address, phone, age, email))
            self.conn.commit()
            messagebox.showinfo("Berhasil", "Pengguna Berhasil dibuat!.")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Isi data dengan benar!.")

    def read_users(self):
        # Clear previous data
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.cursor.execute('SELECT * FROM users')
        users = self.cursor.fetchall()
        for user in users:
            self.tree.insert("", "end", values=user)

    def update_user(self):
        selected_user = self.tree.selection()
        if selected_user:
            user_id = self.tree.item(selected_user, 'values')[0]
            new_name = self.entry_name.get()
            new_address = self.entry_address.get()
            new_phone = self.entry_phone.get()
            new_age = self.entry_age.get()
            new_email = self.entry_email.get()

            if new_name and new_age:
                self.cursor.execute('''
                    UPDATE users 
                    SET name=?, address=?, phone=?, age=?, email=? 
                    WHERE id=?
                ''', (new_name, new_address, new_phone, new_age, new_email, user_id))
                self.conn.commit()
                messagebox.showinfo("Berhasil", "Data berhasil di update.")
                self.clear_entries()
                self.read_users()
            else:
                messagebox.showerror("Error", "Isi data dengan benar!.")
        else:
            messagebox.showerror("Error", "Pilih data untuk diperbarui!")

    def delete_user(self):
        selected_user = self.tree.selection()
        if selected_user:
            user_id = self.tree.item(selected_user, 'values')[0]
            self.cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "User deleted successfully.")
            self.read_users()
        else:
            messagebox.showerror("Error", "Please select a user to delete.")

    def clear_entries(self):
        self.entry_id.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_address.delete(0, END)
        self.entry_phone.delete(0, END)
        self.entry_age.delete(0, END)
        self.entry_email.delete(0, END)

# Run the Tkinter application
if __name__ == "__main__":
    root = Tk()
    app = CRUDApp(root)
    root.mainloop()

# Close the database connection when the GUI is closed
app.conn.close()
