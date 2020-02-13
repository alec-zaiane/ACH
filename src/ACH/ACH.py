from src.ACH.HyperDeck import *
import os
from time import time as time_seconds
from time import sleep
# from multiprocessing import Process
from src.ACH.Replay import *
from tkinter import *

# program start time
pgm_start_time = time_seconds()*1000
# initialize hyperdeck list
hyperdecks = []
# initialize replay List
replays = []
replay_names = []


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


def start_recording():  # TODO this should be async, then we can trust that they will start synchonized
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
    if recording:
        record_duration = time() - record_start_time  # Make sure that the timecode it will save is within the active recording period
        if record_duration > timeoffset_ms:
            replays.append(
                Replay(last_deck_position[0]+record_duration-timeoffset_ms, "replay @" + to_hyperdeck_code(time()-pgm_start_time)))  # TODO Test to make sure, this should work
            sync_replay_names()
        else:
            replays.append(
                Replay(last_deck_position[0] + record_duration, "replay @" + to_hyperdeck_code(time()-pgm_start_time)))  # TODO Test to make sure, this should work
            sync_replay_names()

    else:
        print("Not currently recording")


def sync_replay_names():
    global replay_names
    replay_names = []  # clear all items in replay names list
    # Clear all items in listbox
    listbox.delete(0, END)
    for replay in replays:
        replay_names.append(replay.name)  # add replay name to list
        listbox.insert(END,replay.name)  # add replay name to listbox
    global replay_names_svar
    replay_names_svar = StringVar(value=replay_names)


def recall_replay(replay):
    print("recalling replay " + replay.get_hyperdeck_tc() + " on all Hyperdecks")
    for deck in hyperdecks:
        deck.goto(replay.get_hyperdeck_tc())


def get_latest_time():  # Returns the latest possible time the hyperdeck could jog to at that time
    last_clip_end_ms = []
    for deck in hyperdecks:  # find the last possible timecode of each hyperdeck
        out = deck.send_command("clips get")
        last_clip = out[-32:-8]
        last_clip_start = last_clip[:11]
        last_clip_length = last_clip[:12]
        try:
            last_clip_end_ms.append(to_millis(last_clip_start) + to_millis(last_clip_length))
        except ValueError:
            last_clip_end_ms.append(0)
    # make sure the timecodes are close to each other (<50ms different which would mean they are all within 3 frames of each other)
    if abs(last_clip_end_ms[0] - last_clip_end_ms[1]) > 50:  # TODO make this work with >2 Hyperdecks
        print("ERROR, Hyperdecks are out of sync by " + abs(last_clip_end_ms[0] - last_clip_end_ms[1]) + "ms")
    return last_clip_end_ms


# </editor-fold>

# <editor-fold desc="GUI functions">

def gui_recall_replay_from_list(keypress):
    if recording:
        stop_recording()
    recall_replay(replays[listbox.curselection()[0]])
    send_all_hyperdecks("play: speed:75")


def gui_save_replay(keypress):
    try:
        idx = str(keypress).index("char=")
    except ValueError:
        print("Keypress issue, could not find 'char=' in "+str(keypress))
    key = str(keypress)[idx+6:idx+7]
    save_replay(int(key)*1000)


def gui_start_record(keypress):
    start_recording()


def gui_stop_record(keypress):
    if recording:
        stop_recording()
    else:
        send_all_hyperdecks("stop")
    global replays
    # Delete all old replays because they won't work
    replays = []
    sync_replay_names()
# </editor-fold>


# START OF MAIN ********************************************************************************************************

# Load Hyperdecks from file found two directories up (os.pardir to go up) and in the assets folder (should be OS agnostic)
print("Loading HyperDecks:")
hyperdeck_ip_list = [line.rstrip('\n') for line in
                     open(os.path.join(os.pardir, os.pardir, "assets", "HyperDecks.txt"), "r")]
for ip in hyperdeck_ip_list:
    hyperdecks.append(HyperDeck(ip))
# Test if each Hyperdeck is connected, if not, warn user
for hd in hyperdecks:
    output = hd.test_connection()
    if output == "Error":
        print(str(hd) + " is not reachable")
    else:
        print(str(hd) + " connected")
print("══════════════════════════")


root = Tk()  # Create GUI Window
root.geometry('450x500')  # sets window size
# GUI CODE HERE
# initialize stuff
replay_names_svar = StringVar(value=replay_names)
listbox = Listbox(root, listvariable=replay_names_svar, height=20)
title_lbl = Label(root, text="ACH")
# place everything in a grid layout
title_lbl.grid(column=0, row=0, pady=5)
listbox.grid(column=0, row=1, padx=5)
# colour alternating lines of the listbox TODO not working
# for i in range(0, len(replay_names), 2):
#     listbox.itemconfigure(i, background='#f0f0ff')
# assign keyboard shortcuts

# Bindings
# play and record bindings
root.bind('r', gui_start_record)
root.bind('s', gui_stop_record)

# Recall replays bindings
listbox.bind('<Double-1>', gui_recall_replay_from_list)
root.bind('<Return>', gui_recall_replay_from_list)

# saving replays bindings
root.bind('1', gui_save_replay)
root.bind('2', gui_save_replay)
root.bind('3', gui_save_replay)
root.bind('4', gui_save_replay)
root.bind('5', gui_save_replay)
root.bind('6', gui_save_replay)
root.bind('7', gui_save_replay)
root.bind('8', gui_save_replay)
root.bind('9', gui_save_replay)

listbox.selection_set(0)
root.mainloop()  # Keep the GUI window running
