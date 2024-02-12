from datetime import datetime
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

class Merge_GUI:
    def __init__(self, tk=tk):
        self.root = tk.Tk()
        self.root.attributes('-topmost', 0)

    def validate_filepath(self, filepath, os=os):
        try:
            if os.path.isfile(filepath):
                return True
            else:
                raise FileNotFoundError(f"There is no file at the path: \"{filepath}\".")
        except Exception as err:
            raise Exception(f"An error occurred while checking the filepath:\n{str(err)}")
        
    def validate_directory(self, dirpath, os=os):
        try:
            if os.path.isdir(dirpath):
                return True
            else:
                raise FileNotFoundError(f"There is no directory at the path: \"{dirpath}\".")
        except Exception as err:
            raise Exception(f"An error occurred while checking the directory path:\n{str(err)}")

    def is_midifile(self, filepath, os=os):
        self.validate_filepath(filepath, os=os)
        _, file_extension = os.path.splitext(filepath)
        if file_extension.lower() == ".mid":
            return True
        else:
            raise Exception("MIDI-Merge can only merge *.mid files!")

    def get_old_filepath(self, tk=tk, filedialog=filedialog, os=os):
        tk.messagebox.showinfo(
            icon=None,
            title="Pre-Edit MIDI File Selection",
            message="Select the original multitrack MIDI file using the file dialogue window.",
        )
        old_filepath = filedialog.askopenfilename()
        self.is_midifile(old_filepath, os=os)
        return old_filepath

    def get_in_dir(self, tk=tk, filedialog=filedialog, os=os):
        tk.messagebox.showinfo(
            icon=None,
            title="Stitch Directory",
            message="Select the directory which contains single track MIDI files to be combined together.",
        )
        in_dir = filedialog.askdirectory()
        self.validate_directory(in_dir, os=os)
        return in_dir

    def get_output_filepath(self, tk=tk, filedialog=filedialog, datetime=datetime, os=os):
        tk.messagebox.showinfo(
            icon=None,
            title="Output Directory",
            message="Choose a directory for the output file.\nIt will be named with the date and time in the format DD-MM-YY_hh-mm-ss.midi",
        )
        output_directory = filedialog.askdirectory()
        self.validate_directory(output_directory, os=os)
        output_filepath = (
            output_directory
            + f"/{datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}.mid"
        )
        return output_filepath