import os
from mido import MidiFile, MidiTrack, Message, MetaMessage

class MIDI_Merge:
    def __init__(self, GUI):
        GUI = GUI()
        self.old_filepath = GUI.get_old_filepath()
        self.stitch_directory = GUI.get_in_dir()
        self.out_filepath = GUI.get_output_filepath()

    def run(self):
        """
        Converts a directory full of MIDI format 0 files into a single MIDI format 1 file.
        """
        # Use TKinter to get file and directory paths
        old_multitrack = MidiFile(self.old_filepath)

        new_monotracks = []
        for filepath in (filepaths := os.listdir(self.stitch_directory)):
            new_monotracks.append(MidiFile(self.stitch_directory + f"/{filepath}"))

        ticks_per_beat = 96

        print("Initialising output file...")
        output_midi = MidiFile(ticks_per_beat=ticks_per_beat, type=1)
        print(output_midi.ticks_per_beat)

        output_midi.tracks.append(old_multitrack.tracks[0])
        print(f"Output file initialised with {ticks_per_beat} ticks per beat.")
        new_tracks = []

        for file, filepath in zip(new_monotracks, filepaths):
            print(f"    - Filepath: {filepath}")
            new_track = MidiTrack()

            for track in file.tracks:
                name = track[0].name
                print(f"    - Track: {name}")

                for old_track in old_multitrack.tracks[1:]:
                    if name == old_track[0].name.split("\x00")[0]:
                        channel_number = old_track[1].channel
                        print(f"      Channel: {channel_number}.")

                print("    - Transferring messages...")
                new_track.append(track[0])
                new_track.append(
                    MetaMessage(type="channel_prefix", channel=channel_number, time=0)
                )

                for message in track[3:]:
                    try:
                        message.channel = channel_number
                    except AttributeError:
                        pass
                    new_track.append(message.copy())

            new_tracks.append((new_track, new_track[1].channel))

        # Sort the tracks in new_tracks by channel_number
        print("Sorting tracks by channel number...")
        new_tracks.sort(key=lambda x: x[1])

        print("Adding tracks to output file...")
        for track, channel in new_tracks:
            print(f"    - Track: {track[0].name}")
            print(f"      Channel: {channel}")
            output_midi.tracks.append(track)

        # Save the combined MIDI file
        output_midi.save(self.out_filepath)
        print(f"\nOutput saved at: {self.out_filepath}")