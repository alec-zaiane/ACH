from src.ACH.HyperDeck import*
import os
from time import time as time_seconds
# from multiprocessing import Process
from src.ACH.Replay import *
from tkinter import *

# initialize hyperdeck list
hyperdecks = []
# initialize replay List
replays = []
replay_names =[]

# record_start_time
record_start_time = 0
recording = False
last_deck_position = 0
# ^By calling global later on before referencing any of these vars, it accesses these instead of creating new local ones


# <editor-fold desc="Function definitions">
# define util functions
def add_log(string):
    main_log.append(string)


def print_log_total():
    for entry in main_log:
        print(entry)
        print("══════════════════════════")


def time():
    return int(round(time_seconds() * 1000))


# Function to send a command to a single hyperdeck
def send_hyperdeck(hyperdeck, command):
    hyperdeck.send_command(command)


# Function to send a command simultaneously to every hyperdeck
def send_all_hyperdecks(command):
    processes = []
    # Create multiple processes to send each hyperdeck a command at the same time
    for deck in hyperdecks:
        if deck.connectable:
            send_hyperdeck(deck, command)
    # start each process
    for process in processes:
        process.start()
    # Wait for each process to end
    for process in processes:
        process.join()


def start_recording():
    global last_deck_position
    last_deck_position = get_latest_time()
    send_all_hyperdecks("record")
    global record_start_time
    record_start_time = time()
    global recording
    recording = True


def stop_recording():
    send_all_hyperdecks("stop")
    global recording
    recording = False


def save_replay(timeoffset_ms):
    record_duration = time()-record_start_time  # Make sure that the timecode it will save is within the active recording period
    if record_duration < timeoffset_ms:
        replays.append(Replay(record_start_time + time(), "replay @"+str(time())))  # TODO Test this to make sure it works
        sync_replay_names()


def sync_replay_names():
    global replay_names
    replay_names = []
    for replay in replays:
        replay_names.append(replay.name)


def recall_replay(replay):
    print("DEBUG recalling replay "+replay.get_hyperdeck_tc()+" on all Hyperdecks")
    for deck in hyperdecks:
        deck.goto(replay.get_hyperdeck_tc())


def get_latest_time():  # Returns the latest possible time the hyperdeck could jog to at that time
    last_clip_end_ms = []
    for deck in hyperdecks:  # find the last possible timecode of each hyperdeck
        out = deck.send_command("clips get")
        last_clip = out[-32:-8]
        last_clip_start = last_clip[:11]
        last_clip_length = last_clip[:12]
        last_clip_end_ms.append(to_millis(last_clip_start)+to_millis(last_clip_length))
    # make sure the timecodes are close to each other (<50ms different which would mean they are all within 3 frames of each other)
    if abs(last_clip_end_ms[0] - last_clip_end_ms[1]) > 50:  # TODO make this work with >2 Hyperdecks
        print("ERROR, Hyperdecks are out of sync by "+abs(last_clip_end_ms[0] - last_clip_end_ms[1])+"ms")
    return last_clip_end_ms


# </editor-fold>

# START OF MAIN ********************************************************************************************************

# Load Hyperdecks from file found two directories up (os.pardir to go up) and in the assets folder (should be OS agnostic)
print("Loading HyperDecks:")
hyperdeck_ip_list = [line.rstrip('\n') for line in open(os.path.join(os.pardir, os.pardir, "assets", "HyperDecks.txt"), "r")]
for ip in hyperdeck_ip_list:
    hyperdecks.append(HyperDeck(ip))
# Test if each Hyperdeck is connected, if not, warn user
for hd in hyperdecks:
    output = hd.test_connection()
    if output == "Error":
        print(str(hd)+" is not reachable")
    else:
        print(str(hd)+" connected")
print("══════════════════════════")


root = Tk()  # Create GUI Window
# GUI CODE HERE

root.mainloop()  # Keep the GUI window running
