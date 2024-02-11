import pytest
from unittest.mock import Mock
from lib.midi_merge import MIDI_Merge

GUI_instance = Mock()
GUI_instance.get_old_filepath.return_value = "old_filepath.mid"
GUI_instance.get_in_dir.return_value = "stitch_directory"
GUI_instance.get_output_filepath.return_value = "out_filepath.mid"
GUI = Mock()
GUI.return_value = GUI_instance

ticks_per_beat = 48

os = Mock()
os.listdir.return_value = ["file1.mid", "file2.mid"]

def test_midi_merge_init():
    merger = MIDI_Merge(GUI=GUI, ticks_per_beat=ticks_per_beat, os=os)

    variables = [merger.old_filepath,
             merger.old_multitrack,
             merger.stitch_directory,
             merger.out_filepath,
             merger.output_midi,
             merger.new_monotracks,
             merger.new_tracks,
             merger.filepaths,
             merger.ticks_per_beat]
    
    values = ["old_filepath.mid", 
                 None, 
                 "stitch_directory", 
                 "out_filepath.mid",
                 None,
                 [],
                 [],
                 ["file1.mid", "file2.mid"],
                 ticks_per_beat]
    
    for variable, value in zip(variables, values):
        assert variable == value

def test_midi_merge_create_midifile_objects():
    merge_instance = MIDI_Merge(GUI=GUI, ticks_per_beat=48, os=os)
    MidiFile_instance = Mock()
    MidiFile = Mock()
    MidiFile.return_value = MidiFile_instance
    MidiFile_instance.tracks = ["track1", "track2"]
    merge_instance.create_midifile_objects(MidiFile=MidiFile)

    assert MidiFile.call_count == 4
    assert merge_instance.old_multitrack is not None
    assert len(merge_instance.new_monotracks) == 2
    assert merge_instance.output_midi is not None