import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading
import pyautogui
import cv2
import numpy as np
import os
import time
from PIL import Image, ImageTk
import psutil
import pygetwindow as gw
import csv
import datetime
import subprocess

class ProductivityTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Productivity Tracker')

        self.recording = False
        self.frames = []
        self.productive_time = 18
        self.unproductive_time = 9

        self.create_user_profile()
        self.create_bar_graph()
        self.create_buttons()
        self.create_total_time_label() 
        self.create_update_button()
        
        self.user_name, self.user_id = self.read_current_user_info()
        self.create_logout_button()

        self.report_button = tk.Button(self.profile_frame, text="Report", command=self.open_report)
        self.report_button.pack()

        self.user_id_label = tk.Label(self.profile_frame)  # Replace with actual User ID
        self.user_id_label.pack()

    def create_user_profile(self):
        self.profile_frame = tk.Frame(self.root)
        self.profile_frame.pack(side=tk.RIGHT, padx=20)

        profile_image = Image.open("C:\\Users\\ameyh\\sem5_miniproject\\user.png")  # Replace with your user photo path
        profile_image = profile_image.resize((100, 100), Image.LANCZOS)  # Use LANCZOS
        self.profile_photo = ImageTk.PhotoImage(profile_image)
        self.profile_photo_label = tk.Label(self.profile_frame, image=self.profile_photo)
        self.profile_photo_label.pack()

        self.user_name_label = tk.Label(self.profile_frame, text="Your Name")  # Replace with user's name
        self.user_name_label.pack()

    def create_bar_graph(self):
        self.graph_frame = tk.Frame(self.root)
        self.graph_frame.pack(side=tk.LEFT, padx=20, pady=20)

        categories = ['Productive', 'Unproductive']
        values = [self.productive_time, self.unproductive_time]

        fig, ax = plt.subplots()
        ax.bar(categories, values)
        ax.set_ylabel('Time (minutes)')
        ax.set_title('Productivity Stats')

        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack()

    def create_buttons(self):
        self.start_recording_button = tk.Button(self.profile_frame, text="Start Recording", command=self.start_screen_recording)
        self.start_recording_button.pack()

        self.stop_recording_button = tk.Button(self.profile_frame, text="Stop Recording", command=self.stop_screen_recording, state=tk.DISABLED)
        self.stop_recording_button.pack()

    def create_total_time_label(self):
        self.total_time_label = tk.Label(self.profile_frame, text=f"Total Time: {self.productive_time + self.unproductive_time} minutes")
        self.total_time_label.pack()

    def create_update_button(self):
        self.update_button = tk.Button(self.profile_frame, text="UPDATE", command=self.open_form)
        self.update_button.pack()

    def open_form(self):
        # Run the form.py script
        os.system("python form.py")

    def create_logout_button(self):
        self.logout_button = tk.Button(self.profile_frame, text="Logout", command=self.logout)
        self.logout_button.pack()

    def read_current_user_info(self):
        try:
            with open('current_user.txt', mode='r') as user_file:
                lines = user_file.readlines()
                if len(lines) >= 2:
                    user_name = lines[0].strip()
                    user_id = lines[1].strip()
                    return user_name, user_id
        except FileNotFoundError:
            messagebox.showerror("Error", "current_user.txt not found.")
        return "", ""

    def logout(self):
        # Record the current time as Time_Out
        time_out = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Read the existing data from the CSV file
        data = []
        try:
            with open('entry.csv', mode='r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            pass

        # Find the row with the matching User ID and no Time_Out recorded
        updated = False
        for row in data:
            if 'User ID' in row and 'Time_Out' not in row and row['User ID'] == self.user_id:
                row['Time_Out'] = time_out
                updated = True
                break

        if not updated:
            # If no matching row was found, create a new row
            new_entry = {
                'User Name': self.user_name,
                'User ID': self.user_id,
                'Time_IN': time_out,  # Use Time_IN to store Time_Out for the first entry
                'Time_Out': time_out
            }
            data.append(new_entry)

        # Write the updated data (or new entry) back to the CSV file
        with open('entry.csv', mode='w', newline='') as csvfile:
            fieldnames = ['User Name', 'User ID', 'Time_IN', 'Time_Out']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        messagebox.showinfo("Logout", "Logged out successfully.")

        # Quit the tkinter application
        self.root.quit()


    def open_report(self):
     subprocess.Popen(["python", "report.py"])


    def check_browser_url(self):
        while self.recording:
            # Check if Microsoft Edge is open
            if self.is_edge_open():
                current_url = self.get_edge_url()
                productivity_status = self.check_url_productivity(current_url)
                self.update_graph(productivity_status)
            time.sleep(5)  # Check every 5 seconds

    def is_edge_open(self):
        for process in psutil.process_iter(attrs=['pid', 'name']):
            try:
                process_info = process.info()
                process_name = process_info['name'].lower()
                if 'msedge.exe' in process_name:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def get_edge_url(self):
        edge_window = gw.getWindowsWithTitle("Microsoft Edge")  # Get a list of Microsoft Edge windows
        if edge_window:
            active_window = edge_window[0]  # Assuming the first window is the active one
            active_window.activate()  # Activate the Microsoft Edge window
            pyautogui.hotkey("Ctrl", "l")  # Press Ctrl+L to focus on the address bar
            pyautogui.hotkey("Ctrl", "c")  # Press Ctrl+C to copy the URL to the clipboard
            url = pyautogui.paste()  # Get the copied URL from the clipboard
            return url.strip()
        else:
            return None  # Microsoft Edge is not open or no windows found

    def check_url_productivity(self, url):
        try:
            with open('data.csv', mode='r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['Website URL'] == url:
                        return row['Productivity']  # Return 'productive' or 'unproductive'
        except FileNotFoundError:
            messagebox.showerror("Error", "data.csv not found.")
        return None  # URL not found in data.csv or error occurred

    def update_graph(self, productivity_status):
        if productivity_status == 'productive':
            self.productive_time += 1
        elif productivity_status == 'unproductive':
            self.unproductive_time += 1

        # Update the graph with new data
        categories = ['Productive', 'Unproductive']
        values = [self.productive_time, self.unproductive_time]

        # Clear the existing graph
        self.canvas.get_tk_widget().destroy()

        # Create a new graph
        fig, ax = plt.subplots()
        ax.bar(categories, values)
        ax.set_ylabel('Time (minutes)')
        ax.set_title('Productivity Stats')

        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack()

    def start_screen_recording(self):
        self.recording = True
        self.start_recording_button.config(state=tk.DISABLED)
        self.stop_recording_button.config(state=tk.NORMAL)
        self.frames = []

        self.screen_recorder_thread = threading.Thread(target=self.record_screen)
        self.screen_recorder_thread.start()
        messagebox.showinfo("Recording", "Screen recording started.")

    def stop_screen_recording(self):
        self.recording = False
        self.start_recording_button.config(state=tk.NORMAL)
        self.stop_recording_button.config(state=tk.DISABLED)
        self.frames_to_video("screen_recording.mp4")
        messagebox.showinfo("Recording", "Screen recording stopped.")

    def record_screen(self):
        while self.recording:
            screenshot = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            self.frames.append(frame)
            time.sleep(0.1)

    def frames_to_video(self, video_path):
        if len(self.frames) == 0:
            return

        height, width, layers = self.frames[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, 10, (width, height))

        for frame in self.frames:
            out.write(frame)
        out.release()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductivityTrackerApp(root)
    app.run()
