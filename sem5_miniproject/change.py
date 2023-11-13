import tkinter as tk
from tkinter import messagebox
import csv
import subprocess

# Create a tkinter window
root = tk.Tk()
root.title('Delete Website Entry')

# User Input
website_label = tk.Label(root, text="Enter Website URL:")
website_label.pack()
website_entry = tk.Entry(root)
website_entry.pack()

# Delete Button
def delete_entry():
    website_url = website_entry.get()
    if not website_url:
        messagebox.showerror("Error", "Please enter a website URL.")
        return

    rows = []
    deleted_row = None  # Initialize a variable to store the row to be deleted

    # Read data.csv and find the row to be deleted
    with open('data.csv', mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames  # Get the field names from the CSV
        for row in reader:
            if row['Website URL'] == website_url:
                deleted_row = row  # Store the row to be deleted
            else:
                rows.append(row)

    if deleted_row is None:
        messagebox.showerror("Error", "Website URL not found in data.csv.")
        return

    # Write the rows back to data.csv, excluding the deleted row
    with open('data.csv', mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    messagebox.showinfo("Success", f"Deleted entry for {website_url}")
    website_entry.delete(0, tk.END)  # Clear the input field

delete_button = tk.Button(root, text="Delete", command=delete_entry)
delete_button.pack(pady=10)

# Start the tkinter main loop
root.mainloop()
