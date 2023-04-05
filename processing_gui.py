import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import data_processing

class DataProcessingGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("UTME Data Processing")
        self.master.configure(background="black")

        # Create labels and entry fields
        self.path_label = ttk.Label(master, text="Directory with all .WAV files:")
        self.path_entry = ttk.Entry(master, width=50)
        self.freq_label = ttk.Label(master, text="List of frequencies in Hz(separated by commas):")
        self.freq_entry = ttk.Entry(master, width=50)

        # Create buttons for file dialogs
        self.browse_button = ttk.Button(master, text="Browse", command=self.browse_files)

        # Create button to start playback
        self.plot_button = ttk.Button(master, text="Create Plots", command=self.create_plot)

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Define the accent button style
        self.style.configure("AccentButton.TButton", foreground="white", background="#5e5e5e", font=('Segoe UI', 11))
        self.style.map("AccentButton.TButton", foreground=[("active", "white")], background=[("active", "#444444")])

        # Configure the colors of the other widgets
        self.style.configure("TLabel", foreground="white", background="#1c1c1c", font=('Segoe UI', 11))
        self.style.configure("TEntry", foreground="black", background="#1c1c1c", font=('Segoe UI', 11))
        self.style.configure("TButton", foreground="white", background="#0066cc", font=('Segoe UI', 11))
        self.style.map("TButton", foreground=[("active", "white")], background=[("active", "#0052a3")])

        # Layout widgets using grid
        self.path_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.path_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)
        self.freq_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.freq_entry.grid(row=2, column=1, padx=5, pady=5)
        self.plot_button.grid(row=4, column=1, padx=5, pady=5)

    def browse_files(self):
        file_path = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Folder")
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, file_path)

    def create_plot(self):
        # Your code for playing the MP3 file goes here
        directory = self.path_entry.get()
        filenames = data_processing.get_filenames_in_order(directory)
        for f in filenames:
            print(f)

        frequencies = self.freq_entry.get()
        frequencies = data_processing.parse_freq_input(frequencies)
        print(frequencies)
        
if __name__ == '__main__':
    root = tk.Tk()
    my_gui = DataProcessingGUI(root)
    root.mainloop()
