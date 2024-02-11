import os
from mido import MidiFile, MidiTrack, MetaMessage

class MIDI_Merge:
    def __init__(self, GUI, ticks_per_beat=None, os=os):
        GUI = GUI()

        self.old_filepath = GUI.get_old_filepath()
        self.old_multitrack = None

        self.stitch_directory = GUI.get_in_dir()
        
        self.out_filepath = GUI.get_output_filepath()
        self.output_midi = None

        self.new_monotracks = []
        self.new_tracks = []

        self.filepaths = os.listdir(self.stitch_directory)
        self.ticks_per_beat = ticks_per_beat or 96

    def create_midifile_objects(self, MidiFile=MidiFile):
        self.old_multitrack = MidiFile(self.old_filepath)
        for filepath in (self.filepaths):
            self.new_monotracks.append(MidiFile(self.stitch_directory + f"/{filepath}"))
        self.output_midi = MidiFile(ticks_per_beat=self.ticks_per_beat, type=1)
        self.output_midi.tracks.append(self.old_multitrack.tracks[0])

    def convert_monotrack_files_to_miditrack_objects(self, MidiTrack=MidiTrack, MetaMessage=MetaMessage):
        for file, filepath in zip(self.new_monotracks, self.filepaths):
            print(f"    - Filepath: {filepath}")
            new_track = MidiTrack()

            for track in file.tracks:
                name = track[0].name
                print(f"    - Track: {name}")

                for old_track in self.old_multitrack.tracks[1:]:
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

            self.new_tracks.append((new_track, new_track[1].channel))       
    
    def sort_tracks_by_channel(self):
        print("Sorting tracks by channel number...")
        self.new_tracks.sort(key=lambda x: x[1])
    
    def append_tracks_to_output_file(self):
        print("Adding tracks to output file...")
        for track, channel in self.new_tracks:
            print(f"    - Track: {track[0].name}")
            print(f"      Channel: {channel}")
            self.output_midi.tracks.append(track)

    def write_out(self):
        self.output_midi.save(self.out_filepath)
        print(f"\nOutput saved at: {self.out_filepath}")

    def run(self):
        """
        Converts a directory full of MIDI format 0 files into a single MIDI format 1 file.
        """
        print("MIDI-Merge#run() is deprecated.")
        # Use TKinter to get file and directory paths
        
        # print("Initialising output file...")
        # output_midi = MidiFile(ticks_per_beat=self.ticks_per_beat, type=1)
        # print(output_midi.ticks_per_beat)

        # self.output_midi.tracks.append(self.old_multitrack.tracks[0])
        # print(f"Output file initialised with {self.ticks_per_beat} ticks per beat.")
        # new_tracks = []

        # for file, filepath in zip(self.new_monotracks, self.filepaths):
        #     print(f"    - Filepath: {filepath}")
        #     new_track = MidiTrack()

        #     for track in file.tracks:
        #         name = track[0].name
        #         print(f"    - Track: {name}")

        #         for old_track in self.old_multitrack.tracks[1:]:
        #             if name == old_track[0].name.split("\x00")[0]:
        #                 channel_number = old_track[1].channel
        #                 print(f"      Channel: {channel_number}.")

        #         print("    - Transferring messages...")
        #         new_track.append(track[0])
        #         new_track.append(
        #             MetaMessage(type="channel_prefix", channel=channel_number, time=0)
        #         )

        #         for message in track[3:]:
        #             try:
        #                 message.channel = channel_number
        #             except AttributeError:
        #                 pass
        #             new_track.append(message.copy())

        #     new_tracks.append((new_track, new_track[1].channel))

        # Sort the tracks in new_tracks by channel_number
        # print("Sorting tracks by channel number...")
        # self.new_tracks.sort(key=lambda x: x[1])

        # print("Adding tracks to output file...")
        # for track, channel in self.new_tracks:
        #     print(f"    - Track: {track[0].name}")
        #     print(f"      Channel: {channel}")
        #     self.output_midi.tracks.append(track)

        # Save the combined MIDI file
        # self.output_midi.save(self.out_filepath)
        # print(f"\nOutput saved at: {self.out_filepath}")