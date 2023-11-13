import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import csv
import datetime
import subprocess

# Create a tkinter window
root = tk.Tk()
root.title('Login')

# Load and display the user photo (user.png)
try:
    user_photo = Image.open("user.png")  # Replace with the path to your user photo
    user_photo = user_photo.resize((200, 200), Image.LANCZOS)  # Adjust the size as needed
    user_photo = ImageTk.PhotoImage(user_photo)
    user_photo_label = tk.Label(root, image=user_photo)
    user_photo_label.pack(pady=20)
except FileNotFoundError:
    user_photo_label = tk.Label(root, text="User Photo (user.png) not found.")
    user_photo_label.pack(pady=20)

# User Name
user_name_label = tk.Label(root, text="User Name:")
user_name_label.pack()
user_name_entry = tk.Entry(root)
user_name_entry.pack()

# User ID
user_id_label = tk.Label(root, text="User ID:")
user_id_label.pack()
user_id_entry = tk.Entry(root)
user_id_entry.pack()

# Submit Button
def submit():
    name = user_name_entry.get()
    user_id = user_id_entry.get()

    if name and user_id:
        # Record the current time as Time_IN
        time_in = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save the values to the CSV file
        with open('entry.csv', mode='a', newline='') as csvfile:
            fieldnames = ['User Name', 'User ID', 'Time_IN', 'Time_Out']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the data to the CSV file
            writer.writerow({'User Name': name, 'User ID': user_id, 'Time_IN': time_in, 'Time_Out': ''})

        # Store User Name and User ID in a text file for gui.py
        with open('current_user.txt', mode='w') as user_file:
            user_file.write(f"{name}\n{user_id}")

        root.withdraw()  # Hide the login window
        # Redirect to gui.py
        subprocess.Popen(["python", "gui.py", user_id])  # Pass user_id as an argument to gui.py

    else:
        messagebox.showerror("Error", "Please enter both User Name and User ID.")

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

# Start the tkinter main loop
root.mainloop()
