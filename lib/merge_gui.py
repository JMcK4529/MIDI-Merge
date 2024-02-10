from datetime import datetime
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

class Merge_GUI:
    def __init__(self, tk=tk):
        self.root = tk.Tk()
        self.root.attributes('-topmost', 0)

    def get_old_filepath(self, tk=tk, filedialog=filedialog):
        tk.messagebox.showinfo(
            icon=None,
            title="Pre-Edit MIDI File Selection",
            message="Select the original multitrack MIDI file using the file dialogue window.",
        )
        old_filepath = filedialog.askopenfilename()
        return old_filepath

    def get_in_dir(self, tk=tk, filedialog=filedialog):
        tk.messagebox.showinfo(
            icon=None,
            title="Stitch Directory",
            message="Select the directory which contains single track MIDI files to be combined together.",
        )
        in_dir = filedialog.askdirectory()
        return in_dir

    def get_output_filepath(self, tk=tk, filedialog=filedialog, datetime=datetime):
        tk.messagebox.showinfo(
            icon=None,
            title="Output Directory",
            message="Choose a directory for the output file.\nIt will be named with the date and time in the format DD-MM-YY_hh-mm-ss.midi",
        )
        output_directory = filedialog.askdirectory()
        output_filepath = (
            output_directory
            + f"/{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}.mid"
        )
        return output_filepath