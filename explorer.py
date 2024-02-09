import mido, os, sys, datetime
from mido import MidiFile, MidiTrack, Message, MetaMessage
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

class MIDI_Merge_GUI:
    def __init__(self):
        root = tk.Tk()
        root.attributes('-topmost', 0)

    def get_old_filepath(self):
        tk.messagebox.showinfo(
            icon=None,
            title="Pre-Edit MIDI File Selection",
            message="Select the original multitrack MIDI file using the file dialogue window.",
        )
        old_filepath = filedialog.askopenfilename()
        return old_filepath

    def get_in_dir(self):
        tk.messagebox.showinfo(
            title="Stitch Directory",
            message="Select the directory which contains single track MIDI files to be combined together.",
        )
        in_dir = filedialog.askdirectory()
        return in_dir

    def get_output_filepath(self):
        tk.messagebox.showinfo(
            title="Output Directory",
            message="Choose a directory for the output file.\nIt will be named with the date and time in the format DD-MM-YY_hh-mm-ss.midi",
        )
        output_directory = filedialog.askdirectory()
        output_filepath = (
            output_directory
            + f"/{datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}.mid"
        )
        return output_filepath

class MIDI_Merge:
    def __init__(self):
        GUI = MIDI_Merge_GUI()
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


if __name__ == "__main__":
    app = MIDI_Merge()
    app.run()


# out_filepath = "output.mid"
# # import old multitrack
# old_multitrack = MidiFile("./KRONOS_MIDI_OUT/TEST MIDI 4 JOE/BERLIN CITY TOUR.mid")
# # import new monotracks
# new_monotracks = []
# print(os.listdir("./KRONOS_MIDI_OUT/TEST MIDI 4 JOE/Stitch/"))
# for filepath in (filepaths := os.listdir("./KRONOS_MIDI_OUT/TEST MIDI 4 JOE/Stitch/")):
#     new_monotracks.append(MidiFile("./KRONOS_MIDI_OUT/TEST MIDI 4 JOE/Stitch/" + filepath))
# # get the ticks per beat for the multitrack
# ticks_per_beat = 96 # old_multitrack.ticks_per_beat or 480
# # for each monotrack, find the track in the multitrack which has the same name
# print("Initialising output file...")
# output_midi = MidiFile(ticks_per_beat=ticks_per_beat, type=1)
# print(output_midi.ticks_per_beat)
# output_midi.tracks.append(old_multitrack.tracks[0])
# print(f"Output file initialised with {ticks_per_beat} ticks per beat.")
# new_tracks = []
# print("Working on:")
# for file, filepath in zip(new_monotracks, filepaths):
#     print(f"    - Filepath: {filepath}")
#     new_track = MidiTrack()
#     for track in file.tracks:
#         name = track[0].name
#         print(f"    - Track: {name}")
#         for old_track in old_multitrack.tracks[1:]:
#             # in that track within the multitrack, find a message that has a channel attribute
#             if name == old_track[0].name.split('\x00')[0]:
#                 channel_number = old_track[1].channel
#                 print(f"      Channel: {channel_number}.")
#         print("    - Transferring messages...")
#         new_track.append(track[0])
#         new_track.append(MetaMessage(type='channel_prefix', channel=channel_number, time=0))
#         for message in track[3:]:
#             # use try/except AttributeError to apply that channel number to each message in the monotrack
#             try:
#                 message.channel = channel_number
#             except AttributeError:
#                 pass
#             # then copy the monotrack to a new_track and append the new_track to the output file
#             new_track.append(message.copy())
#     new_tracks.append((new_track, new_track[1].channel))

# # Sort the tracks in new_tracks by channel_number
# print("Sorting tracks by channel number...")
# new_tracks.sort(key=lambda x: x[1])

# print("Adding tracks to output file...")
# for (track, channel) in new_tracks:
#     print(f"    - Track: {track[0].name}")
#     print(f"      Channel: {channel}")
#     output_midi.tracks.append(track)

# # Save the combined MIDI file
# output_midi.save(out_filepath)
# print(f"\nOutput saved at: {out_filepath}")

# with open("old_multi.txt", "w") as file:
#     file.write(str(old_multitrack))

# with open("new_multi.txt", "w") as file:
#     file.write(str(output_midi))

# with open("mono1.txt", "w") as file:
#     file.write(str(new_monotracks[0]))

# with open("mono2.txt", "w") as file:
#     rnb2 = MidiFile("./KRONOS_MIDI_OUT/TEST MIDI 4 JOE/R&B Kit2.mid")
#     file.write(str(rnb2))
