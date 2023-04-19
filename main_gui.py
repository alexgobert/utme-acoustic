from tkinter import Tk, ttk, filedialog, END
from os import getcwd
from driver import main
from serial.tools.list_ports import comports, grep
from SignalProcessing import process_files
from arduino_controller import create_commands
from functools import reduce
from datetime import timedelta
from mutagen.mp3 import MP3

class AcousticDirectivityDriverGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("UTME Acoustic Directivity Driver")
        self.master.configure(background="black")
        
        self.ports = comports()

        # Create labels and entry fields
        self.path_label = ttk.Label(master, text="Path to mp3 file to be played:")
        self.path_entry = ttk.Entry(master, width=50)
        self.rotation_label = ttk.Label(master, text="Rotation Increment (degrees):")
        self.rotation_entry = ttk.Entry(master)
        self.recording_label = ttk.Label(master, text="Path to store .WAV recording:")
        self.recording_entry = ttk.Entry(master, width=50)
        self.port_label = ttk.Label(master, text='Arduino Port:')
        self.port_entry = ttk.Combobox(master, values=self.ports, width=45)
        self.freq_label = ttk.Label(master, text='Frequency to plot:')
        self.freq_entry = ttk.Entry(master)
        self.estimate_label = ttk.Label(master, text='')

        # Create buttons for file dialogs
        self.browse_button = ttk.Button(master, text="Browse", command=self.browse_files)
        self.recording_browse_button = ttk.Button(master, text="Browse", command=self.browse_recording_path)

        # Create button to start playback
        self.play_button = ttk.Button(master, text="Play", command=self.start_test)
        self.estimate_button = ttk.Button(master, text='Estimate Time', command=self.estimate_time)
        self.process_button = ttk.Button(master, text='Plot Only', command=self.start_processing)

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
        self.play_button.grid(row=6, column=1, padx=0, pady=5)
        self.process_button.grid(row=7, column=1, padx=5, pady=5)
        self.estimate_button.grid(row=6, column=2, padx=0, pady=5)
        self.estimate_label.grid(row=7, column=2, padx=5, pady=5)


    def browse_files(self):
        file_path = filedialog.askopenfilename(initialdir=getcwd(), title="Select File", filetypes=(("MP3 Files", "*.mp3"),))
        self.path_entry.delete(0, END)
        self.path_entry.insert(0, file_path)

    def browse_recording_path(self):
        recording_path = filedialog.askdirectory(initialdir=getcwd(), title="Select Folder")
        self.recording_entry.delete(0, END)
        self.recording_entry.insert(0, recording_path)

    def start_test(self):
        if not self.fields_filled():
            # TODO: input validation
            return

        mp3 = self.path_entry.get()
        rec_path = self.recording_entry.get()
        angleStep = int(self.rotation_entry.get())
        # port = next(grep(self.port_entry.get())).device
        port = 'COM7'
        freq = int(self.freq_entry.get())

        main(mp3, rec_path, angleStep, freq, port)

    def start_processing(self):
        if not all((self.is_int(self.rotation_entry.get()), self.is_int(self.freq_entry.get()), self.recording_entry.get())):
            # TODO: error message
            return

        rec_path = self.recording_entry.get()
        angleStep = int(self.rotation_entry.get())
        freq = int(self.freq_entry.get())

        process_files(angleStep, freq, rec_path)

    def estimate_time(self):
        if not all((self.is_int(self.rotation_entry.get()), self.path_entry.get())):
            # TODO: error message
            return
        
        angleStep = int(self.rotation_entry.get())
        mp3 = self.path_entry.get()

        commands, _ = create_commands(angleStep)

        time = reduce(lambda x, y: x + y[0], commands, 0)
        time += MP3(mp3).info.length * 360 / angleStep

        time = str(timedelta(seconds=int(time)))

        self.estimate_label.config(text=self.format_date(time))


    def fields_filled(self) -> bool:
        return all((
            self.is_int(self.rotation_entry.get()),
            self.is_int(self.freq_entry.get()),
            self.path_entry.get(),
            self.recording_entry.get(),
            self.port_entry.get()
        ))
    
    @classmethod
    def is_int(cls, val) -> bool:
        try:
            int(val)
        except:
            return False
        
        return True
    
    @classmethod
    def format_date(cls, strng: str) -> str:
        FIELDS = ('Hours', 'Minutes', 'Seconds')

        lst = strng.strip().split(':')
        zipped = zip(lst, FIELDS)
        
        return ', '.join(' '.join(elem) for elem in zipped)
        

if __name__ == '__main__':
    root = Tk()
    my_gui = AcousticDirectivityDriverGUI(root)
    root.mainloop()
