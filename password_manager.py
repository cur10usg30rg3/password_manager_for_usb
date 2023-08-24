import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askstring
import random
import string
import tkinter.messagebox as messagebox

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry('600x600')
        self.root.configure(bg='#2C3E50')  # Background color
       
        self.real_passwords = {} # Initialize the real_passwords dictionary
        self.passwords_hidden = True  # Initialize this attribute to True, indicating that passwords are initially hidden


        style = ttk.Style(self.root)
        style.configure("Treeview", background="#34495E", fieldbackground="#34495E", foreground="white")
        style.map('Treeview', background=[('selected', '#3E4E55')])
        style.configure("Treeview.Heading", background="#2C3E50", foreground="black")

        self.tree = ttk.Treeview(self.root, columns=("Name", "Username", "Password"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.pack(padx=10, pady=10, expand=True, fill='both')
    
        # Create a frame to hold the buttons and center-align them
        button_frame = tk.Frame(self.root, bg='#2C3E50')  # Create a frame to hold the buttons
        button_frame.pack(side='bottom', pady=20)

        button_width = 20  # Specify a fixed width for the buttons

        self.add_button = tk.Button(button_frame, text="Add", command=self.add_entry, width=button_width, bg='#2980B9', fg='white')  
        self.add_button.grid(row=0, column=0, padx=5, pady=5)

        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_entry, width=button_width, bg='#2980B9', fg='white')
        self.delete_button.grid(row=1, column=0, padx=5, pady=5)

        self.show_password_button = tk.Button(button_frame, text="Show Passwords", command=self.show_selected_password, width=button_width, bg='#2980B9', fg='white')
        self.show_password_button.grid(row=0, column=1, padx=5, pady=5)

        self.modify_button = tk.Button(button_frame, text="Modify", command=self.modify_entry, width=button_width, bg='#2980B9', fg='white')
        self.modify_button.grid(row=1, column=1, padx=5, pady=5)
    
        # Load data (if applicable)
        self.load_data()
    
        # Set up the function to call on closing the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_control_buttons(self):
        self.show_password_button = tk.Button(self.root, text="Show Passwords", command=self.show_selected_password, bg='#2980B9', fg='white')
        self.show_password_button.pack(side='bottom', pady=5)

        self.add_button = tk.Button(self.root, text="Add", command=self.add_entry, bg='#2980B9', fg='white')
        self.add_button.pack(side='bottom', padx=10, pady=5)

    def add_entry(self):
        name = askstring("Enter Service Name", "Service Name:")
        username = askstring("Enter Username", "Username:")
        if (name, username) in self.real_passwords:
            messagebox.showinfo("Duplicate Username", "This username already exists for the service.")
            return

        password_length = askstring("Choose Password Length", "Enter password length:")
        try:
            password_length = int(password_length)
            if password_length < 8:
                messagebox.showinfo("Invalid Length", "Password length should be at least 8.")
                return
        except (ValueError, TypeError):
            messagebox.showinfo("Invalid Length", "Defaulting to password length of 8.")
            password_length = 8

        custom_password = askstring("Custom Password", "Enter a custom password (leave blank to generate one):", show='*')
        if custom_password:
            generated_password = custom_password
        else:
            generated_password = self.generate_password(password_length)

        self.real_passwords[(name, username)] = generated_password  # Save with tuple as the key
        self.tree.insert("", "end", values=(name, username, self.mask_password(generated_password)))

    def generate_password(self, length):
        characters = string.ascii_letters + string.digits + string.punctuation
        while True:
            password = ''.join(random.choice(characters) for _ in range(length))
            if (any(c.islower() for c in password) and 
                any(c.isupper() for c in password) and 
                any(c.isdigit() for c in password) and 
                any(c in string.punctuation for c in password)):
                break
        return password
    
    def save_data(self):
        with open("passwords.txt", "w") as f:
            for item in self.tree.get_children():
                name, username, _ = self.tree.item(item, "values")
                f.write(f"{name} | {username} | {self.real_passwords[(name, username)]}\n")

    def load_data(self):
        try:
            with open("passwords.txt", "r") as f:
                for line in f:
                    name, username, password = line.strip().split(" | ")
                    self.real_passwords[(name, username)] = password
                    self.tree.insert("", "end", values=(name, username, self.mask_password(password)))
        except FileNotFoundError:
            pass
        except Exception as e:
            messagebox.showerror("Error", f"Could not load data: {e}")

    def mask_password(self, password):
        return '*' * len(password)
    
    def modify_entry(self):
        selected_item = self.tree.selection()[0]
        if selected_item:
            name, username, _ = self.tree.item(selected_item, "values")
            if (name, username) not in self.real_passwords:
                messagebox.showinfo("Error", "The selected entry is not in the database.")
                return
        
            new_name = askstring("Modify Service Name", "Service Name:", initialvalue=name)
            new_username = askstring("Modify Username", "Username:", initialvalue=username)
        
            if (new_name, new_username) in self.real_passwords and (new_name, new_username) != (name, username):
                messagebox.showinfo("Duplicate Entry", "This username already exists for the service.")
                return

            if new_name and new_username:
                password = self.real_passwords.pop((name, username))
                self.real_passwords[(new_name, new_username)] = password
                self.tree.item(selected_item, values=(new_name, new_username, self.mask_password(password)))

    
    def delete_entry(self):
        selected_item = self.tree.selection()[0]
        if selected_item:
            name, username, _ = self.tree.item(selected_item, "values")
            del self.real_passwords[(name, username)]
            self.tree.delete(selected_item)

    def show_selected_password(self):
        selected_items = self.tree.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]  # Get selected item
        values = self.tree.item(selected_item, "values")

        if values:
            name, username, _ = values
            real_password = self.real_passwords.get((name, username), "")
            if self.passwords_hidden:
                self.tree.item(selected_item, values=(name, username, real_password))
            else:
                self.tree.item(selected_item, values=(name, username, self.mask_password(real_password)))

        self.passwords_hidden = not self.passwords_hidden  # Toggle the status
        self.show_password_button.config(text="Hide Passwords" if not self.passwords_hidden else "Show Passwords")



    def on_closing(self):
        self.save_data()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()
