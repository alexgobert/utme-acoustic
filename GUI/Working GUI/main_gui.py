import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import audio_utils

class AcousticDirectivityDriverGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("UTME Acoustic Directivity Driver")
        self.master.configure(background="black")

        # Create labels and entry fields
        self.path_label = ttk.Label(master, text="Path to mp3 file to be played:")
        self.path_entry = ttk.Entry(master, width=50)
        self.rotation_label = ttk.Label(master, text="Rotation Increment (degrees):")
        self.rotation_entry = ttk.Entry(master)
        self.recording_label = ttk.Label(master, text="Path to store .WAV recording:")
        self.recording_entry = ttk.Entry(master, width=50)

        # Create buttons for file dialogs
        self.browse_button = ttk.Button(master, text="Browse", command=self.browse_files)
        self.recording_browse_button = ttk.Button(master, text="Browse", command=self.browse_recording_path)

        # Create button to start playback
        self.play_button = ttk.Button(master, text="Play", command=self.play_file)

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
        self.rotation_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.rotation_entry.grid(row=2, column=1, padx=5, pady=5)
        self.recording_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.recording_entry.grid(row=1, column=1, padx=5, pady=5)
        self.recording_browse_button.grid(row=1, column=2, padx=5, pady=5)
        self.play_button.grid(row=4, column=1, padx=5, pady=5)

    def browse_files(self):
        file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File", filetypes=(("MP3 Files", "*.mp3"),))
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, file_path)

    def browse_recording_path(self):
        recording_path = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Folder")
        self.recording_entry.delete(0, tk.END)
        self.recording_entry.insert(0, recording_path)

    def play_file(self):
        # Your code for playing the MP3 file goes here
        mp3 = self.path_entry.get()
        print(mp3)
        rec_path = self.recording_entry.get()
        print(rec_path)

        audio_utils.run_threads(mp3, rec_path)
        
        

if __name__ == '__main__':
    root = tk.Tk()
    my_gui = AcousticDirectivityDriverGUI(root)
    root.mainloop()
