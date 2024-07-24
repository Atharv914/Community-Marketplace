import sqlite3  # Import the sqlite3 library to interact with the SQLite database
import tkinter as tk  # Import the tkinter library for creating GUI applications
from tkinter import messagebox  # Import the messagebox from tkinter for displaying message boxes
import datetime  # Import the datetime module to work with date and time

'''
Created on Jul 15, 2024

@author: Atharv Kundoori
'''

# Database setup
def setup_db():
    conn = sqlite3.connect('community_marketplace.db')  # Connect to the SQLite database named 'community_marketplace.db'
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    
    # Create the 'users' table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password TEXT,
                        contact_info TEXT)''')

    # Create the 'items' table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        name TEXT,
                        category TEXT,
                        price REAL,
                        description TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')

    # Create the 'messages' table if it doesn't exist
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

    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the database connection

# User management functions
def register_user(username, password, contact_info):
    try:
        conn = sqlite3.connect('community_marketplace.db')  # Connect to the SQLite database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands
        # Insert the new user into the 'users' table
        cursor.execute("INSERT INTO users (username, password, contact_info) VALUES (?, ?, ?)",
                       (username, password, contact_info))
        conn.commit()  # Commit the changes to the database
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")  # Show an error message if the username already exists
    finally:
        conn.close()  # Close the database connection

def login_user(username, password):
    conn = sqlite3.connect('community_marketplace.db')  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    # Select the user from the 'users' table where the username and password match
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()  # Fetch one result
    conn.close()  # Close the database connection
    return user  # Return the user

# Item listing functions
def add_item(user_id, name, category, price, description):
    try:
        conn = sqlite3.connect('community_marketplace.db')  # Connect to the SQLite database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands
        # Insert the new item into the 'items' table
        cursor.execute("INSERT INTO items (user_id, name, category, price, description) VALUES (?, ?, ?, ?, ?)",
                       (user_id, name, category, price, description))
        conn.commit()  # Commit the changes to the database
    except sqlite3.OperationalError:
        messagebox.showerror("Error", "Database is locked. Please try again.")  # Show an error message if the database is locked
    finally:
        conn.close()  # Close the database connection

def get_items():
    conn = sqlite3.connect('community_marketplace.db')  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    cursor.execute("SELECT * FROM items")  # Select all items from the 'items' table
    items = cursor.fetchall()  # Fetch all results
    conn.close()  # Close the database connection
    return items  # Return the list of items

def search_items(keyword):
    conn = sqlite3.connect('community_marketplace.db')  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    # Select items from the 'items' table where the name, category, or description matches the keyword
    cursor.execute("SELECT * FROM items WHERE name LIKE ? OR category LIKE ? OR description LIKE ?",
                   ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))
    items = cursor.fetchall()  # Fetch all results
    conn.close()  # Close the database connection
    return items  # Return the list of matching items

# Messaging functions
def send_message(sender_id, receiver_id, item_id, message):
    try:
        conn = sqlite3.connect('community_marketplace.db')  # Connect to the SQLite database
        cursor = conn.cursor()  # Create a cursor object to execute SQL commands
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current timestamp
        # Insert the new message into the 'messages' table
        cursor.execute("INSERT INTO messages (sender_id, receiver_id, item_id, message, timestamp) VALUES (?, ?, ?, ?, ?)",
                       (sender_id, receiver_id, item_id, message, timestamp))
        conn.commit()  # Commit the changes to the database
    except sqlite3.OperationalError:
        messagebox.showerror("Error", "Database is locked. Please try again.")  # Show an error message if the database is locked
    finally:
        conn.close()  # Close the database connection

def get_messages(user_id):
    conn = sqlite3.connect('community_marketplace.db')  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor object to execute SQL commands
    # Select messages from the 'messages' table where the receiver_id matches the user_id
    cursor.execute("SELECT * FROM messages WHERE receiver_id = ?", (user_id,))
    messages = cursor.fetchall()  # Fetch all results
    conn.close()  # Close the database connection
    return messages  # Return the list of messages

# GUI setup
def register_user_ui():
    def register():
        username = entry_username.get()  # Get the username from the entry field
        password = entry_password.get()  # Get the password from the entry field
        contact_info = entry_contact_info.get()  # Get the contact information from the entry field
        register_user(username, password, contact_info)  # Register the user
        messagebox.showinfo("Success", "User registered successfully")  # Show a success message
        register_window.destroy()  # Close the register window

    register_window = tk.Toplevel(root)  # Create a new top-level window for registration
    register_window.title("Register User")  # Set the title of the window
    
    tk.Label(register_window, text="Username").pack()  # Create a label for the username
    entry_username = tk.Entry(register_window)  # Create an entry field for the username
    entry_username.pack()  # Pack the entry field
    
    tk.Label(register_window, text="Password").pack()  # Create a label for the password
    entry_password = tk.Entry(register_window, show='*')  # Create an entry field for the password with masked input
    entry_password.pack()  # Pack the entry field
    
    tk.Label(register_window, text="Contact Info").pack()  # Create a label for the contact information
    entry_contact_info = tk.Entry(register_window)  # Create an entry field for the contact information
    entry_contact_info.pack()  # Pack the entry field
    
    tk.Button(register_window, text="Register", command=register).pack()  # Create a register button and pack it

def login_user_ui():
    def login():
        username = entry_username.get()  # Get the username from the entry field
        password = entry_password.get()  # Get the password from the entry field
        user = login_user(username, password)  # Attempt to log in the user
        if user:
            messagebox.showinfo("Success", "Login successful")  # Show a success message if login is successful
            login_window.destroy()  # Close the login window
            main_app_ui(user[0])  # Open the main application window
        else:
            messagebox.showerror("Error", "Invalid username or password")  # Show an error message if login fails

    login_window = tk.Toplevel(root)  # Create a new top-level window for login
    login_window.title("Login User")  # Set the title of the window
    
    tk.Label(login_window, text="Username").pack()  # Create a label for the username
    entry_username = tk.Entry(login_window)  # Create an entry field for the username
    entry_username.pack()  # Pack the entry field
    
    tk.Label(login_window, text="Password").pack()  # Create a label for the password
    entry_password = tk.Entry(login_window, show='*')  # Create an entry field for the password with masked input
    entry_password.pack()  # Pack the entry field
    
    tk.Button(login_window, text="Login", command=login).pack()  # Create a login button and pack it

def main_app_ui(user_id):
    def add_item_ui():
        def add():
            name = entry_name.get()  # Get the item name from the entry field
            category = entry_category.get()  # Get the item category from the entry field
            price = entry_price.get()  # Get the item price from the entry field
            price = price.replace('$', '').replace(',', '').strip()  # Remove $ and commas from the price
            try:
                price = float(price)  # Convert the price to a float
            except ValueError:
                messagebox.showerror("Error", "Invalid price format")  # Show an error message if the price format is invalid
                return
            description = entry_description.get()  # Get the item description from the entry field
            add_item(user_id, name, category, price, description)  # Add the item to the database
            messagebox.showinfo("Success", "Item added successfully")  # Show a success message
            add_window.destroy()  # Close the add item window

        add_window = tk.Toplevel(root)  # Create a new top-level window for adding an item
        add_window.title("Add Item")  # Set the title of the window
        
        tk.Label(add_window, text="Item Name").pack()  # Create a label for the item name
        entry_name = tk.Entry(add_window)  # Create an entry field for the item name
        entry_name.pack()  # Pack the entry field
        
        tk.Label(add_window, text="Category").pack()  # Create a label for the category
        entry_category = tk.Entry(add_window)  # Create an entry field for the category
        entry_category.pack()  # Pack the entry field
        
        tk.Label(add_window, text="Price").pack()  # Create a label for the price
        entry_price = tk.Entry(add_window)  # Create an entry field for the price
        entry_price.pack()  # Pack the entry field
        
        tk.Label(add_window, text="Description").pack()  # Create a label for the description
        entry_description = tk.Entry(add_window)  # Create an entry field for the description
        entry_description.pack()  # Pack the entry field
        
        tk.Button(add_window, text="Add", command=add).pack()  # Create an add button and pack it

    def view_items_ui():
        items = get_items()  # Get all items from the database
        view_window = tk.Toplevel(root)  # Create a new top-level window for viewing items
        view_window.title("View Items")  # Set the title of the window
        
        for item in items:
            # Create a label for each item and pack it
            tk.Label(view_window, text=f"Name: {item[2]}, Category: {item[3]}, Price: ${item[4]:.2f}, Description: {item[5]}").pack()

    def search_items_ui():
        def search():
            keyword = entry_keyword.get()  # Get the keyword from the entry field
            items = search_items(keyword)  # Search for items matching the keyword
            search_window = tk.Toplevel(root)  # Create a new top-level window for search results
            search_window.title("Search Results")  # Set the title of the window
            
            for item in items:
                # Create a label for each search result and pack it
                tk.Label(search_window, text=f"Name: {item[2]}, Category: {item[3]}, Price: ${item[4]:.2f}, Description: {item[5]}").pack()

        search_window = tk.Toplevel(root)  # Create a new top-level window for searching items
        search_window.title("Search Items")  # Set the title of the window
        
        tk.Label(search_window, text="Keyword").pack()  # Create a label for the keyword
        entry_keyword = tk.Entry(search_window)  # Create an entry field for the keyword
        entry_keyword.pack()  # Pack the entry field
        
        tk.Button(search_window, text="Search", command=search).pack()  # Create a search button and pack it

    main_window = tk.Toplevel(root)  # Create a new top-level window for the main application
    main_window.title("Community Marketplace")  # Set the title of the window
    
    tk.Button(main_window, text="Add Item", command=add_item_ui).pack()  # Create an add item button and pack it
    tk.Button(main_window, text="View Items", command=view_items_ui).pack()  # Create a view items button and pack it
    tk.Button(main_window, text="Search Items", command=search_items_ui).pack()  # Create a search items button and pack it

root = tk.Tk()  # Create the root window
root.title("Community Marketplace")  # Set the title of the window

tk.Button(root, text="Register", command=register_user_ui).pack()  # Create a register button and pack it
tk.Button(root, text="Login", command=login_user_ui).pack()  # Create a login button and pack it

# Call setup_db to initialize the database and create tables
setup_db()  # Initialize the database

root.mainloop()  # Run the main event loop of the application
