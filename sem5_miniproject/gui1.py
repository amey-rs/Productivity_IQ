import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Sample data from "productive or unproductive data.csv"
data = pd.read_csv("productive or unproductive data.csv")

# Strip column names to remove leading/trailing whitespaces
data.columns = data.columns.str.strip()

class ProductivityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Productivity Search")

        self.create_controls()
        self.create_chart()

    def create_controls(self):
        username_label = ttk.Label(self.root, text="Enter UserName:")
        username_label.pack()

        self.username_entry = ttk.Entry(self.root)
        self.username_entry.pack()

        search_button = ttk.Button(self.root, text="Search", command=self.search_productivity)
        search_button.pack()

    def create_chart(self):
        self.fig, (self.ax_pie, self.ax_bar) = plt.subplots(1, 2, figsize=(10, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

    def search_productivity(self):
        username = self.username_entry.get()
        username = username.strip()

        if username == "":
            messagebox.showinfo("Invalid Input", "Please enter a valid username.")
            return

        # Search for the username in the dataset
        user_data = data[data['UserName'] == username]

        if user_data.empty:
            messagebox.showinfo("User Not Found", "Username not found in the dataset.")
            return

        # Check if the user is marked as "Productive" or "Unproductive" in the dataset
        productivity_status = user_data['Productive'].values[0]

        # Get the actual time spent for the entire week from the dataset
        total_time_spent = user_data['TimeSpent in week(Hours)'].values[0]

        # Create random time spent for each day of the week
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        time_spent = [random.uniform(0, 10) for _ in days]

        # Ensure that the total time spent for the week remains the same
        total_time_spent = total_time_spent
        time_spent = [time * (total_time_spent / sum(time_spent)) for time in time_spent]

        # Create a color map for productivity and unproductivity
        colors = ['#4CAF50', '#FF5733']  # Green for Productive, Red for Unproductive

        # Create a bar chart for time spent by day of the week
        self.ax_bar.clear()
        self.ax_bar.bar(days, time_spent, color=colors[0])
        self.ax_bar.set_ylabel('Hours')
        self.ax_bar.set_title('Time Spent')

        # Create a pie chart for productivity and unproductivity
        labels = ['Productive', 'Unproductive']
        productivity_score = random.uniform(0.7, 1.0)
        unproductivity_score = random.uniform(0.0, 0.3)
        if productivity_status == "Unproductive":
            productivity_score, unproductivity_score = unproductivity_score, productivity_score  # Swap values
        sizes = [total_time_spent * productivity_score, total_time_spent * unproductivity_score]
        self.ax_pie.clear()
        self.ax_pie.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        self.ax_pie.axis('equal')
        self.ax_pie.set_title(f"Productivity for {username}")

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductivityApp(root)
    root.mainloop()
