# Import all necessary packages
import sqlite3  # Import sqlite for database
import Start_project_Init  # Define all the functions used here
import Psw_save  # Goes to another section where all the passwords are kept (encrypted)
import Psw_save_Init  # Defines all functions for the password_keeper
import Cryptography_Init  # Defines all the functions for encrypting, decrypting getting and setting the keys, etc.
from tkinter import *  # Used for the graphical user interface (gui)
from tkinter import messagebox
import os

# Create main root window and configuring it
root = Tk()
root.title("Login / Signup")
root.iconbitmap("Static/PM.ico")
width = 500
height = 300
root.geometry(str(width) + "x" + str(height))
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width/2) - (width/2))
y_coordinate = int((screen_height/2) - (height/2))
root.geometry(str(width) + "x" + str(height) + "+" + str(x_coordinate) + "+" + str(y_coordinate))

# Create Labels and Adjust them in main window
welcome_label = Label(root, text="Welcome!", font=("Times New Roman", 30))
welcome_label.grid(row=1, column=3, columnspan=100, padx=10, pady=10)
username_label = Label(root, text="Username:", font=("Times New Roman", 15))
username_label.grid(row=5, column=3, padx=3, pady=10)
password_label = Label(root, text="Password:", font=("Times New Roman", 15))
password_label.grid(row=7, column=3, padx=3, pady=10)

# Create Entry and Adjust them in main window
username_entry = Entry(root, width=50)
username_entry.grid(row=5, column=5, columnspan=2)
password_entry = Entry(root, width=50)
password_entry.grid(row=7, column=5, columnspan=2)

# Commands for buttons
def login():
    if (username_entry.get() == "" or password_entry.get() == ""):
        messagebox.showwarning("Warning", "The username or password fields are blank!")
    else:
        username = username_entry.get()  # gets username
        password = password_entry.get()  # gets password
        try:
            key = Cryptography_Init.get_key(username)  # Gets the key for the specified user
            # Because the username and password where encrypted when inserting into table we need to compare them
            if Start_project_Init.searchUser(key, username, password) == True:
                root.destroy()
                Psw_save.mainPasswordKeeper(username)  # We give all the necessary parameters
            else:
                messagebox.showerror("Error", "User has not been found. Please try again, or create an account.")
        except Exception as error:
            messagebox.showerror("Error", error)

def signup():
    if (username_entry.get() == "" or password_entry.get() == ""):
        messagebox.showwarning("Warning", "The username or password fields are blank!")
    else:
        try:
            Start_project_Init.tableCreate()  # Searches to see if database has all ready been created
        except sqlite3.OperationalError as error:
            messagebox.showwarning("Error", error)
        username = username_entry.get()  # gets username
        password = password_entry.get()  # gets password
        try:
            Cryptography_Init.set_key(username)  # sets key for encryption for specified user
            encrypted_user = Cryptography_Init.encrypt_some(username, password)  # encrypts user and password
            encrypted_username = encrypted_user[0]
            encrypted_password = encrypted_user[1]
            Start_project_Init.signup(encrypted_username,
                                 encrypted_password)  # creates record in first table with encrypted data
            Psw_save_Init.createTable(username)  # Creates second table for that specified user
            root.destroy()
            Psw_save.mainPasswordKeeper(username)  # We give all the necessary parameters
        except Exception as error:
            messagebox.showwarning("Error", error)

def info():
    os.system('notepad Static/about.txt')

# Create Buttons and Adjust them in main window
login_button = Button(root, text="Log In", font=("Times New Roman", 13), command=login)
login_button.grid(row=20, column=4, pady=15)
signup_button = Button(root, text="Sign Up", font=("Times New Roman", 13), command=signup)
signup_button.grid(row=20, column=6, pady=15)
info_button = Button(root, text="Info", font=("Times New Roman", 13), command=info)
info_button.grid(row=1000, column=5, padx=15, pady=15)

root.mainloop()

