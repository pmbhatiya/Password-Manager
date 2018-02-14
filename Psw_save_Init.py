import sqlite3
from cryptography.fernet import Fernet
import Psw_save
from tkinter import *  # Used for the graphical user interface (gui)
from tkinter import messagebox

# Query the DB and returning ALL records
def show_all(key, username):
    # Get key
    f = Fernet(key)

    # Connect to database
    conn = sqlite3.connect("PM.db")

    # Create a cursor
    c = conn.cursor()

    # Query database
    c.execute("SELECT rowid, * FROM " + username)
    items = c.fetchall()

    # Create window to show results
    root = Tk()
    root.title("Your Passwords:")
    root.iconbitmap("Static/PM.ico")
    width = 600
    height = 800
    root.geometry(str(width) + "x" + str(height))
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))
    root.geometry(str(width) + "x" + str(height) + "+" + str(x_coordinate) + "+" + str(y_coordinate))

    sb = Scrollbar(root)
    sb.pack(side=RIGHT, fill=Y)
    mylist = Listbox(root, yscrollcommand=sb.set, width=width, height=(height-20))

    # Show results
    for item in items:
        # Decrypt and decode info
        decrypted_user = f.decrypt(item[1])
        original_user = decrypted_user.decode()

        decrypted_pass = f.decrypt(item[2])
        original_pass = decrypted_pass.decode()

        decrypted_email = f.decrypt(item[3])
        original_email = decrypted_email.decode()

        decrypted_info = f.decrypt(item[4])
        original_info = decrypted_info.decode()

        # Format results

        mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        mylist.insert(END, "Id: " + str(item[0]))
        mylist.insert(END, "User/Website: " + original_user)
        mylist.insert(END, "Password: " + original_pass)
        mylist.insert(END, "Email: " + original_email)
        mylist.insert(END, "Info: " + original_info)
        mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        mylist.insert(END, "")

    def go_back():
        root.destroy()
        Psw_save.mainPasswordKeeper(username)

    Button(root, text="Return", command=go_back).pack()

    mylist.pack(side=LEFT)
    sb.config(command=mylist.yview)

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()


# Add ONE new record to the table
def add_one(username, user, password, email, info):
    # Connect to database
    conn = sqlite3.connect("PM.db")

    # Create a cursor
    c = conn.cursor()

    # Query database
    c.execute("INSERT INTO " + username + " VALUES (?, ?, ?, ?)", (user, password, email, info))

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()


# Delete record from table
def delete_one(username, id_var):
    # Connect to database
    conn = sqlite3.connect("PM.db")

    # Create a cursor
    c = conn.cursor()

    # Query database
    c.execute("DELETE from " + username + " WHERE rowid = " + id_var)

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()


# Lookup with WHERE
def name_lookup(key, username, name):
    # Get key
    f = Fernet(key)

    # Connect to database
    conn = sqlite3.connect("PM.db")

    # Create a cursor
    c = conn.cursor()

    # Query database
    c.execute("SELECT rowid, * FROM " + username)
    items = c.fetchall()

    toplvl = Toplevel()
    toplvl.title("Search...")
    toplvl.iconbitmap("Static/PM.ico")
    width = 600
    height = 800
    screen_width = toplvl.winfo_screenwidth()
    screen_height = toplvl.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))
    toplvl.geometry(str(width) + "x" + str(height))
    toplvl.geometry(str(width) + "x" + str(height) + "+" + str(x_coordinate) + "+" + str(y_coordinate))

    sb = Scrollbar(toplvl)
    sb.pack(side=RIGHT, fill=Y)
    mylist = Listbox(toplvl, yscrollcommand=sb.set, width=width, height=(height - 20))

    # Searches through all items
    for item in items:
        # Decrypts the name of the record
        decrypted_name = f.decrypt(item[1])  # The rowid is in the '0' position, so name is in '1'
        original_name = decrypted_name.decode()

        # Compares the record to what the user entered
        if original_name == name:
            decrypted_pass = f.decrypt(item[2])
            original_pass = decrypted_pass.decode()

            decrypted_email = f.decrypt(item[3])
            original_email = decrypted_email.decode()

            decrypted_info = f.decrypt(item[4])
            original_info = decrypted_info.decode()

            # Format results
            mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            mylist.insert(END, "Id: " + str(item[0]))
            mylist.insert(END, "User/Website: " + original_name)
            mylist.insert(END, "Password: " + original_pass)
            mylist.insert(END, "Email: " + original_email)
            mylist.insert(END, "Info: " + original_info)
            mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            mylist.insert(END, "")

    def go_back():
        toplvl.destroy()

    Button(toplvl, text="Return", command=go_back).pack()

    mylist.pack(side=LEFT)
    sb.config(command=mylist.yview)

    toplvl.mainloop()

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()

def id_lookup(key, username, id):
    # Get key
    f = Fernet(key)

    # Connect to database
    conn = sqlite3.connect("PM.db")

    # Create a cursor
    c = conn.cursor()

    # Query database
    c.execute("SELECT rowid, * FROM " + username + " WHERE rowid = (?)", id)
    items = c.fetchall()

    toplvl = Toplevel()
    toplvl.title("Search...")
    toplvl.iconbitmap("Static/PM.ico")
    width = 600
    height = 800
    screen_width = toplvl.winfo_screenwidth()
    screen_height = toplvl.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))
    toplvl.geometry(str(width) + "x" + str(height))
    toplvl.geometry(str(width) + "x" + str(height) + "+" + str(x_coordinate) + "+" + str(y_coordinate))

    try:
        # Searches through all items
        for item in items:
            decrypted_name = f.decrypt(item[1])
            original_name = decrypted_name.decode()

            # Compares the record to what the user entered
            if int(id) == item[0]:  # The rowid is in the '0' position
                decrypted_pass = f.decrypt(item[2])
                original_pass = decrypted_pass.decode()

                decrypted_email = f.decrypt(item[3])
                original_email = decrypted_email.decode()

                decrypted_info = f.decrypt(item[4])
                original_info = decrypted_info.decode()

                # Format results
                info = "Id: " + str(item[0]) + "\n" + "User/Website: " + original_name + "\n" + "Password: " + original_pass \
                               + "\n" + "Email: " + original_email + "\n\n" + "Info: " + original_info

                Label(toplvl, text=info, font=("Times New Roman", 15)).pack()
    except:
        messagebox.showerror("Error", "There is no registry with that ID.")


    def go_back():
        toplvl.destroy()

    Button(toplvl, text="Return", font=("Times New Roman", 15), command=go_back).pack()

    toplvl.mainloop()

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()

def email_lookup(key, username, email):
    # Get key
    f = Fernet(key)

    # Connect to database
    conn = sqlite3.connect("PM.db")

    # Create a cursor
    c = conn.cursor()

    # Query database
    c.execute("SELECT rowid, * FROM " + username)
    items = c.fetchall()

    toplvl = Toplevel()
    toplvl.title("Search...")
    toplvl.iconbitmap("Static/PM.ico")
    width = 600
    height = 800
    screen_width = toplvl.winfo_screenwidth()
    screen_height = toplvl.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))
    toplvl.geometry(str(width) + "x" + str(height))
    toplvl.geometry(str(width) + "x" + str(height) + "+" + str(x_coordinate) + "+" + str(y_coordinate))

    sb = Scrollbar(toplvl)
    sb.pack(side=RIGHT, fill=Y)
    mylist = Listbox(toplvl, yscrollcommand=sb.set, width=width, height=(height - 20))

    # Searches through all items
    for item in items:
        # Decrypts the name of the record
        decrypted_name = f.decrypt(item[1])  # The rowid is in the '0' position, so name is in '1'
        original_name = decrypted_name.decode()

        decrypted_email = f.decrypt(item[3])  # The email is in position '3'
        original_email = decrypted_email.decode()

        # Compares the record to what the user entered
        if original_email == email:
            decrypted_pass = f.decrypt(item[2])
            original_pass = decrypted_pass.decode()

            decrypted_info = f.decrypt(item[4])
            original_info = decrypted_info.decode()

            # Format results
            mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            mylist.insert(END, "Id: " + str(item[0]))
            mylist.insert(END, "User/Website: " + original_name)
            mylist.insert(END, "Password: " + original_pass)
            mylist.insert(END, "Email: " + original_email)
            mylist.insert(END, "Info: " + original_info)
            mylist.insert(END, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            mylist.insert(END, "")

    def go_back():
        toplvl.destroy()

    Button(toplvl, text="Return", command=go_back).pack()

    mylist.pack(side=LEFT)
    sb.config(command=mylist.yview)

    toplvl.mainloop()

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()

# Update record
def update_one(username, user, password, email, info, id):
    # Connect to database
    conn = sqlite3.connect("PM.db")

    # Create a cursor
    c = conn.cursor()

    c.execute(" UPDATE " + username + " SET username = (?) WHERE rowid = (?)", (user, id))
    c.execute(" UPDATE " + username + " SET password = (?) WHERE rowid = (?)", (password, id))
    c.execute(" UPDATE " + username + " SET email = (?) WHERE rowid = (?)", (email, id))
    c.execute(" UPDATE " + username + " SET info = (?) WHERE rowid = (?)", (info, id))


    # Commit changes to db
    conn.commit()

    # Close connection to db
    conn.close()

# Creates table for specific user
def createTable(username):
    connection = sqlite3.connect("PM.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE " + username + "(username text, password text, email text, info text)")
    connection.commit()
    connection.close()
