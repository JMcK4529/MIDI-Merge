from unittest.mock import Mock
import tkinter as tk
import pytest
from datetime import datetime
from lib.merge_gui import Merge_GUI

def test_merge_gui_init():
    GUI = Merge_GUI()
    assert isinstance(GUI.root, tk.Tk)

def test_merge_gui_validate_filepath():
    GUI = Merge_GUI()
    example_filepath = "some_filepath.mid"
    mock_os = Mock()
    mock_os.path.isfile.return_value = True
    assert GUI.validate_filepath(example_filepath, os=mock_os) == True

    not_found_error = FileNotFoundError(f"There is no file at the path: \"{example_filepath}\".")
    mock_os.path.isfile.return_value = False
    with pytest.raises(Exception) as err:
        GUI.validate_filepath(example_filepath, os=mock_os)
    assert str(err.value) == f"An error occurred while checking the filepath:\n{str(not_found_error)}"

def test_merge_gui_validate_directory():
    GUI = Merge_GUI()
    example_dirpath = "./some_dir/some_other_dir"
    mock_os = Mock()
    mock_os.path.isdir.return_value = True
    assert GUI.validate_filepath(example_dirpath, os=mock_os) == True

    not_found_error = FileNotFoundError(f"There is no directory at the path: \"{example_dirpath}\".")
    mock_os.path.isdir.return_value = False
    with pytest.raises(Exception) as err:
        GUI.validate_directory(example_dirpath, os=mock_os)
    assert str(err.value) == f"An error occurred while checking the directory path:\n{str(not_found_error)}"

def test_merge_gui_is_midifile():
    GUI = Merge_GUI()
    example_filepath = "./stitch_directory/SOME_FILE.MID"
    mock_os = Mock()
    mock_os.path.isfile.return_value = True
    mock_os.path.splitext.return_value = ("useless path sections", ".MID")
    assert GUI.is_midifile(example_filepath, os=mock_os)

    example_filepath = "not_a_midifile.txt"
    mock_os.path.splitext.return_value = ("useless path sections", ".txt")
    _, file_extension = ("useless path sections", ".MID")
    print(file_extension)
    with pytest.raises(Exception) as err:
        GUI.is_midifile(example_filepath, os=mock_os)
    assert str(err.value) == f"MIDI-Merge can only merge *.mid files!"

def test_merge_gui_get_old_filepath():
    GUI = Merge_GUI()
    old_filepath = "old_filepath.mid"
    mock_tk = Mock()
    mock_tk.messagebox.showinfo = Mock()
    mock_filedialog = Mock()
    mock_filedialog.askopenfilename.return_value = old_filepath
    mock_os = Mock()
    mock_os.path.isfile.return_value = True
    mock_os.path.splitext.return_value = ["old_filepath", ".mid"]
    assert GUI.get_old_filepath(tk=mock_tk, filedialog=mock_filedialog, os=mock_os) == old_filepath
    mock_tk.messagebox.showinfo.assert_called_once_with(
        icon=None,
        title="Pre-Edit MIDI File Selection",
        message="Select the original multitrack MIDI file using the file dialogue window.",
    )

def test_merge_gui_get_in_dir():
    GUI = Merge_GUI()
    in_dir = "in_dir"
    mock_tk = Mock()
    mock_tk.messagebox.showinfo = Mock()
    mock_filedialog = Mock()
    mock_filedialog.askdirectory.return_value = in_dir
    mock_os = Mock()
    mock_os.path.isdir.return_value = True
    assert GUI.get_in_dir(tk=mock_tk, filedialog=mock_filedialog, os=mock_os) == in_dir
    mock_tk.messagebox.showinfo.assert_called_once_with(
        icon=None,
        title="Stitch Directory",
        message="Select the directory which contains single track MIDI files to be combined together.",
    )

def test_merge_gui_get_in_dir_not_found():
    GUI = Merge_GUI()
    in_dir = "in_dir"
    mock_tk = Mock()
    mock_tk.messagebox.showinfo = Mock()
    mock_filedialog = Mock()
    mock_filedialog.askdirectory.return_value = in_dir
    mock_os = Mock()
    mock_os.path.isdir.return_value = False
    with pytest.raises(Exception) as err:
        GUI.get_in_dir(tk=mock_tk, filedialog=mock_filedialog, os=mock_os)
    assert str(err.value) == f"An error occurred while checking the directory path:\nThere is no directory at the path: \"{in_dir}\"."

def test_merge_gui_get_output_filepath():
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

    mock_os = Mock()
    mock_os.path.isdir.return_value = True

    assert GUI.get_output_filepath(tk=mock_tk, filedialog=mock_filedialog, datetime=mock_datetime, os=mock_os) == f"{out_dir}/{now}.mid"
    mock_tk.messagebox.showinfo.assert_called_once_with(
        icon=None,
        title="Output Directory",
        message="Choose a directory for the output file.\nIt will be named with the date and time in the format DD-MM-YY_hh-mm-ss.midi",
    )
    today.strftime.assert_called_once_with('%Y-%m-%d_%H-%M-%S')

def test_merge_gui_get_output_filepath_dir_not_found():
    GUI = Merge_GUI()
    output_directory = "out_dir"
    mock_tk = Mock()
    mock_tk.messagebox.showinfo = Mock()
    mock_filedialog = Mock()
    mock_filedialog.askdirectory.return_value = output_directory
    mock_os = Mock()
    mock_os.path.isdir.return_value = False
    with pytest.raises(Exception) as err:
        GUI.get_in_dir(tk=mock_tk, filedialog=mock_filedialog, os=mock_os)
    assert str(err.value) == f"An error occurred while checking the directory path:\nThere is no directory at the path: \"{output_directory}\"."