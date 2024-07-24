import sqlite3
import tkinter as tk
from tkinter import messagebox
import datetime

'''
Created on Jul 15, 2024

@author: Atharv Kundooi
'''

# Database setup
def setup_db():
    conn = sqlite3.connect('community_marketplace.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password TEXT,
                        contact_info TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        name TEXT,
                        category TEXT,
                        price REAL,
                        description TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY,
                        sender_id INTEGER,
                        receiver_id INTEGER,
                        item_id INTEGER,
                        message TEXT,
                        timestamp TEXT,
                        FOREIGN KEY(sender_id) REFERENCES users(id),
                        FOREIGN KEY(receiver_id) REFERENCES users(id),
                        FOREIGN KEY(item_id) REFERENCES items(id))''')

    conn.commit()
    conn.close()

# User management functions
def register_user(username, password, contact_info):
    try:
        conn = sqlite3.connect('community_marketplace.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, contact_info) VALUES (?, ?, ?)",
                       (username, password, contact_info))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect('community_marketplace.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Item listing functions
def add_item(user_id, name, category, price, description):
    try:
        conn = sqlite3.connect('community_marketplace.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (user_id, name, category, price, description) VALUES (?, ?, ?, ?, ?)",
                       (user_id, name, category, price, description))
        conn.commit()
    except sqlite3.OperationalError:
        messagebox.showerror("Error", "Database is locked. Please try again.")
    finally:
        conn.close()

def get_items():
    conn = sqlite3.connect('community_marketplace.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return items

def search_items(keyword):
    conn = sqlite3.connect('community_marketplace.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items WHERE name LIKE ? OR category LIKE ? OR description LIKE ?",
                   ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    items = cursor.fetchall()
    conn.close()
    return items

# Messaging functions
def send_message(sender_id, receiver_id, item_id, message):
    try:
        conn = sqlite3.connect('community_marketplace.db')
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO messages (sender_id, receiver_id, item_id, message, timestamp) VALUES (?, ?, ?, ?, ?)",
                       (sender_id, receiver_id, item_id, message, timestamp))
        conn.commit()
    except sqlite3.OperationalError:
        messagebox.showerror("Error", "Database is locked. Please try again.")
    finally:
        conn.close()

def get_messages(user_id):
    conn = sqlite3.connect('community_marketplace.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE receiver_id = ?", (user_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages

# GUI setup
def register_user_ui():
    def register():
        username = entry_username.get()
        password = entry_password.get()
        contact_info = entry_contact_info.get()
        register_user(username, password, contact_info)
        messagebox.showinfo("Success", "User registered successfully")
        register_window.destroy()

    register_window = tk.Toplevel(root)
    register_window.title("Register User")
    
    tk.Label(register_window, text="Username").pack()
    entry_username = tk.Entry(register_window)
    entry_username.pack()
    
    tk.Label(register_window, text="Password").pack()
    entry_password = tk.Entry(register_window, show='*')
    entry_password.pack()
    
    tk.Label(register_window, text="Contact Info").pack()
    entry_contact_info = tk.Entry(register_window)
    entry_contact_info.pack()
    
    tk.Button(register_window, text="Register", command=register).pack()

def login_user_ui():
    def login():
        username = entry_username.get()
        password = entry_password.get()
        user = login_user(username, password)
        if user:
            messagebox.showinfo("Success", "Login successful")
            login_window.destroy()
            main_app_ui(user[0])
        else:
            messagebox.showerror("Error", "Invalid username or password")

    login_window = tk.Toplevel(root)
    login_window.title("Login User")
    
    tk.Label(login_window, text="Username").pack()
    entry_username = tk.Entry(login_window)
    entry_username.pack()
    
    tk.Label(login_window, text="Password").pack()
    entry_password = tk.Entry(login_window, show='*')
    entry_password.pack()
    
    tk.Button(login_window, text="Login", command=login).pack()

def main_app_ui(user_id):
    def add_item_ui():
        def add():
            name = entry_name.get()
            category = entry_category.get()
            price = entry_price.get()
            price = price.replace('$', '').replace(',', '').strip()  # Remove $ and commas
            try:
                price = float(price)
            except ValueError:
                messagebox.showerror("Error", "Invalid price format")
                return
            description = entry_description.get()
            add_item(user_id, name, category, price, description)
            messagebox.showinfo("Success", "Item added successfully")
            add_window.destroy()

        add_window = tk.Toplevel(root)
        add_window.title("Add Item")
        
        tk.Label(add_window, text="Item Name").pack()
        entry_name = tk.Entry(add_window)
        entry_name.pack()
        
        tk.Label(add_window, text="Category").pack()
        entry_category = tk.Entry(add_window)
        entry_category.pack()
        
        tk.Label(add_window, text="Price").pack()
        entry_price = tk.Entry(add_window)
        entry_price.pack()
        
        tk.Label(add_window, text="Description").pack()
        entry_description = tk.Entry(add_window)
        entry_description.pack()
        
        tk.Button(add_window, text="Add", command=add).pack()

    def view_items_ui():
        items = get_items()
        view_window = tk.Toplevel(root)
        view_window.title("View Items")
        
        for item in items:
            tk.Label(view_window, text=f"Name: {item[2]}, Category: {item[3]}, Price: ${item[4]:.2f}, Description: {item[5]}").pack()

    def search_items_ui():
        def search():
            keyword = entry_keyword.get()
            items = search_items(keyword)
            search_window = tk.Toplevel(root)
            search_window.title("Search Results")
            
            for item in items:
                tk.Label(search_window, text=f"Name: {item[2]}, Category: {item[3]}, Price: ${item[4]:.2f}, Description: {item[5]}").pack()

        search_window = tk.Toplevel(root)
        search_window.title("Search Items")
        
        tk.Label(search_window, text="Keyword").pack()
        entry_keyword = tk.Entry(search_window)
        entry_keyword.pack()
        
        tk.Button(search_window, text="Search", command=search).pack()

    main_window = tk.Toplevel(root)
    main_window.title("Community Marketplace")
    
    tk.Button(main_window, text="Add Item", command=add_item_ui).pack()
    tk.Button(main_window, text="View Items", command=view_items_ui).pack()
    tk.Button(main_window, text="Search Items", command=search_items_ui).pack()

root = tk.Tk()
root.title("Community Marketplace")

tk.Button(root, text="Register", command=register_user_ui).pack()
tk.Button(root, text="Login", command=login_user_ui).pack()

# Call setup_db to initialize the database and create tables
setup_db()

root.mainloop()
