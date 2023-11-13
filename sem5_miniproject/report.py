import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import subprocess
import calendar
 
class HeatmapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Heatmap and Radar Graph Generator")


        self.months = list(calendar.month_abbr)[1:]
        self.weeks = ["1st", "2nd", "3rd", "4th", "Last"]

        self.weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.times = ["Morning", "Afternoon", "Evening"]

        self.create_controls()
        self.create_heatmap()
        self.create_radar_graph()  # Add radar graph initialization

    def create_controls(self):

        month_label = ttk.Label(self.root, text="Select Month:")
        month_label.pack()
        self.selected_month = ttk.Combobox(self.root, values=self.months)
        self.selected_month.pack()

        week_label = ttk.Label(self.root, text="Select Week:")
        week_label.pack()
        self.selected_week = ttk.Combobox(self.root, values=self.weeks)
        self.selected_week.pack()

        weekday_label = ttk.Label(self.root, text="Select Weekday:")
        weekday_label.pack()
        self.selected_weekday = ttk.Combobox(self.root, values=self.weekdays)
        self.selected_weekday.pack()

        time_label = ttk.Label(self.root, text="Select Time of Day:")
        time_label.pack()
        self.selected_time = ttk.Combobox(self.root, values=self.times)
        self.selected_time.pack()

        generate_button = ttk.Button(self.root, text="Generate Heatmap and Radar Graph", command=self.generate_visualizations)
        generate_button.pack()

    def create_heatmap(self):
        self.fig_heatmap, self.ax_heatmap = plt.subplots(figsize=(8, 6))
        self.canvas_heatmap = FigureCanvasTkAgg(self.fig_heatmap, master=self.root)
        self.canvas_heatmap.get_tk_widget().pack()

    def create_radar_graph(self):
        self.fig_radar, self.ax_radar = plt.subplots(figsize=(8, 6))
        self.canvas_radar = FigureCanvasTkAgg(self.fig_radar, master=self.root)
        self.canvas_radar.get_tk_widget().pack()

    def generate_visualizations(self):
        weekday = self.selected_weekday.get()
        time = self.selected_time.get()

        # Generate a sample heatmap data (replace this with your data)
        heatmap_data = np.random.rand(5, 3)

        # Generate radar graph data (replace with your actual data)
        websites = ["Gmail", "Github", "Medium", "Cisco Tracker", "Another Website"]
        interaction_scores = np.random.randint(1, 6, len(websites))

        # Clear previous figures and axes
        self.ax_heatmap.clear()
        self.fig_heatmap.clear()
        self.ax_radar.clear()
        self.fig_radar.clear()

        # Create the heatmap
        self.create_heatmap_plot(heatmap_data)

        # Create the radar graph
        self.create_radar_plot(websites, interaction_scores)

        self.fig_heatmap.canvas.draw()
        self.fig_radar.canvas.draw()

    def create_heatmap_plot(self, heatmap_data):
        self.ax_heatmap = self.fig_heatmap.add_subplot(111)
        heatmap = self.ax_heatmap.imshow(heatmap_data, cmap='coolwarm', interpolation='nearest', aspect='auto')

        self.ax_heatmap.set_xticks(np.arange(len(self.times)))
        self.ax_heatmap.set_yticks(np.arange(len(self.weekdays)))
        self.ax_heatmap.set_xticklabels(self.times)
        self.ax_heatmap.set_yticklabels(self.weekdays)

        plt.setp(self.ax_heatmap.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        self.fig_heatmap.colorbar(heatmap)

    def create_radar_plot(self, websites, scores):
        categories = websites
        N = len(categories)

        angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()

        # Ensure that scores have the same length as angles
        scores += scores[:1]  # Add the first score to the end to close the radar plot

        self.ax_radar = self.fig_radar.add_subplot(111, polar=True)
        self.ax_radar.fill(angles, scores, 'b', alpha=0.1)

        self.ax_radar.set_xticks(angles)
        self.ax_radar.set_xticklabels(categories)
        self.ax_radar.set_yticklabels([])  # Hide radial labels
        self.ax_radar.set_title("Website Interaction Radar Plot")

if __name__ == "__main__":
    root = tk.Tk()
    app = HeatmapApp(root)
    root.mainloop()
