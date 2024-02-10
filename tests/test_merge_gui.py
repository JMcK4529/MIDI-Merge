from unittest.mock import Mock
import tkinter as tk
from datetime import datetime
from lib.merge_gui import Merge_GUI

def test_merge_gui_init():
    GUI = Merge_GUI()
    assert isinstance(GUI.root, tk.Tk)

def test_get_old_filepath_as_intended():
    GUI = Merge_GUI()
    old_filepath = "old_filepath.mid"
    mock_tk = Mock()
    mock_tk.messagebox.showinfo = Mock()
    mock_filedialog = Mock()
    mock_filedialog.askopenfilename.return_value = old_filepath
    assert GUI.get_old_filepath(tk=mock_tk, filedialog=mock_filedialog) == old_filepath
    mock_tk.messagebox.showinfo.assert_called_once_with(
        icon=None,
        title="Pre-Edit MIDI File Selection",
        message="Select the original multitrack MIDI file using the file dialogue window.",
    )

def test_get_in_dir_as_intended():
    GUI = Merge_GUI()
    in_dir = "in_dir"
    mock_tk = Mock()
    mock_tk.messagebox.showinfo = Mock()
    mock_filedialog = Mock()
    mock_filedialog.askdirectory.return_value = in_dir
    assert GUI.get_in_dir(tk=mock_tk, filedialog=mock_filedialog) == in_dir
    mock_tk.messagebox.showinfo.assert_called_once_with(
        icon=None,
        title="Stitch Directory",
        message="Select the directory which contains single track MIDI files to be combined together.",
    )

def test_get_output_filepath_as_intended():
    GUI = Merge_GUI()
    out_dir = "out_dir"
    now = "2024-02-10_09-30-01"

    mock_tk = Mock()
    mock_tk.messagebox.showinfo = Mock()

    mock_filedialog = Mock()
    mock_filedialog.askdirectory.return_value = out_dir

    mock_datetime = Mock()
    today = mock_datetime.today.return_value = Mock()
    today.strftime = Mock(return_value=now)

    assert GUI.get_output_filepath(tk=mock_tk, filedialog=mock_filedialog, datetime=mock_datetime) == f"{out_dir}/{now}.mid"
    mock_tk.messagebox.showinfo.assert_called_once_with(
        icon=None,
        title="Output Directory",
        message="Choose a directory for the output file.\nIt will be named with the date and time in the format DD-MM-YY_hh-mm-ss.midi",
    )
    today.strftime.assert_called_once_with('%Y-%m-%d_%H-%M-%S')