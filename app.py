import mido
from mido import MidiFile, MidiTrack

def get_ticks_per_beat(filepaths):
    midi_files = []
    for filepath in filepaths:
        midi_files.append(midi_file := MidiFile(filepath))
        print(f"\n{filepath}: {midi_file}\ndict: {midi_file.__dict__}\n")
    tpb_list = []
    for file in midi_files:
        tpb_list.append(file.ticks_per_beat)
    if len(set(tpb_list)) == 1:
        print(tpb_list[0])
        return tpb_list[0]
    return 480

def convert_to_format1(midi_files, output_file, ticks_per_beat):
    # Create a new MIDI file with format 1
    output_midi = MidiFile(ticks_per_beat=ticks_per_beat, type=1)

    for i, midi_file_path in enumerate(midi_files):
        # Open each input MIDI file
        input_midi = MidiFile(midi_file_path)

        for track in input_midi.tracks:
            new_track = MidiTrack()
            output_midi.tracks.append(new_track)

            for msg in track:
                # Copy each message from the input file to the new track
                try:
                    if i == 0:
                        msg.channel = 0
                except AttributeError:
                    pass
                new_track.append(msg.copy())
    
    print(f"OUTPUT: {output_midi}")
    # Save the combined MIDI file
    output_midi.save(output_file)

if __name__ == "__main__":
    # List of input MIDI files in format 0
    input_files = ["tracks/C.mid", "tracks/E.mid", "tracks/G.mid"]

    # Output MIDI file in format 1
    output_file = "Cmajor.mid"

    # Convert and save
    convert_to_format1(input_files, output_file, ticks_per_beat=get_ticks_per_beat(input_files))