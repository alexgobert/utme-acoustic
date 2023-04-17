from tkinter import Tk, ttk, filedialog, END
from os import getcwd
from driver import main
from serial.tools.list_ports import comports

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
        self.port_label = ttk.Label(master, text='Arduino Port:')
        self.port_entry = ttk.Combobox(master, values=self.getPorts(), width=45)
        self.freq_label = ttk.Label(master, text='Frequency to plot:')
        self.freq_entry = ttk.Entry(master)

        # Create buttons for file dialogs
        self.browse_button = ttk.Button(master, text="Browse", command=self.browse_files)
        self.recording_browse_button = ttk.Button(master, text="Browse", command=self.browse_recording_path)

        # Create button to start playback
        self.play_button = ttk.Button(master, text="Play", command=self.start_test)

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
        self.port_label.grid(row=4, column=0, padx=5, pady=5)
        self.port_entry.grid(row=4, column=1, padx=5, pady=5)
        self.freq_label.grid(row=5, column=0, padx=5, pady=5)
        self.freq_entry.grid(row=5, column=1, padx=5, pady=5)
        self.play_button.grid(row=6, column=1, padx=5, pady=5)

    def browse_files(self):
        file_path = filedialog.askopenfilename(initialdir=getcwd(), title="Select File", filetypes=(("MP3 Files", "*.mp3"),))
        self.path_entry.delete(0, END)
        self.path_entry.insert(0, file_path)

    def browse_recording_path(self):
        recording_path = filedialog.askdirectory(initialdir=getcwd(), title="Select Folder")
        self.recording_entry.delete(0, END)
        self.recording_entry.insert(0, recording_path)

    def start_test(self):
        if not all((self.isInt(self.rotation_entry.get()), self.isInt(self.freq_entry.get()))):
            # TODO: input validation
            return

        mp3 = self.path_entry.get()
        rec_path = self.recording_entry.get()
        angleStep = int(self.rotation_entry.get())
        port = self.port_entry.get()[-5:-1] # substring to get COM name
        freq = int(self.freq_entry.get())

        main(mp3, rec_path, angleStep, freq, port)

    @classmethod
    def isInt(cls, val) -> bool:
        try:
            int(val)
        except:
            return False
        
        return True

    @classmethod
    def getPorts(cls) -> list:
        return [port.description for port in comports()]
        
        

if __name__ == '__main__':
    root = Tk()
    my_gui = AcousticDirectivityDriverGUI(root)
    root.mainloop()
