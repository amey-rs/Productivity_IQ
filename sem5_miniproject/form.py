import tkinter as tk
from tkinter import messagebox
import csv
from PIL import Image, ImageTk
import os
import subprocess

class DataForm:
    def __init__(self, root):
        self.root = root
        self.root.title('Data Form')

        self.create_user_profile()
        self.create_form()

    def create_user_profile(self):
        self.profile_frame = tk.Frame(self.root)
        self.profile_frame.pack(side=tk.RIGHT, padx=20)

        try:
            profile_image = Image.open("C:\\Users\\ameyh\\sem5_miniproject\\user.png")  # Replace with your user photo path
            profile_image = profile_image.resize((100, 100), Image.LANCZOS)  # Use LANCZOS
            self.profile_photo = ImageTk.PhotoImage(profile_image)
            self.profile_photo_label = tk.Label(self.profile_frame, image=self.profile_photo)
            self.profile_photo_label.pack()
        except FileNotFoundError:
            messagebox.showerror("Error", "User photo (user.png) not found.")


    def create_form(self):
        self.form_frame = tk.Frame(self.root)
        self.form_frame.pack(padx=20, pady=20)

        self.user_name_label = tk.Label(self.form_frame, text="Enter Your Name:")
        self.user_name_label.pack()
        self.user_name_entry = tk.Entry(self.form_frame)
        self.user_name_entry.pack()

        self.website_url_label = tk.Label(self.form_frame, text="Enter Website URL:")
        self.website_url_label.pack()
        self.website_url_entry = tk.Entry(self.form_frame)
        self.website_url_entry.pack()

        self.productivity_label = tk.Label(self.form_frame, text="Select Productivity:")
        self.productivity_label.pack()
        self.productivity_var = tk.StringVar()
        self.productivity_var.set("productive")  # Default to productive
        self.productivity_dropdown = tk.OptionMenu(self.form_frame, self.productivity_var, "productive", "unproductive")
        self.productivity_dropdown.pack()

        self.submit_button = tk.Button(self.form_frame, text="Submit", command=self.save_to_csv)
        self.submit_button.pack()

        self.change_button = tk.Button(self.form_frame, text="Change", command=self.open_change_form)
        self.change_button.pack()


    def save_to_csv(self):
        name = self.user_name_entry.get()
        website_url = self.website_url_entry.get()
        productivity = self.productivity_var.get()

        if name and website_url:
            with open('data.csv', mode='a', newline='') as csvfile:
                fieldnames = ['Name', 'Website URL', 'Productivity']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'Name': name, 'Website URL': website_url, 'Productivity': productivity})
                messagebox.showinfo("Success", "Data saved to data.csv")
                self.clear_fields()
        else:
            messagebox.showerror("Error", "Name and Website URL are required fields.")

    def clear_fields(self):
        self.user_name_entry.delete(0, tk.END)
        self.website_url_entry.delete(0, tk.END)
        self.productivity_var.set("productive")  # Reset to productive


    def open_change_form(self):
        # Run the change.py script
        os.system("python change.py")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataForm(root)
    root.mainloop()
