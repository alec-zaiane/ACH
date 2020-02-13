from src.ACH.HyperDeckClass import*
import os
from time import time,sleep
from multiprocessing import Process
from src.ACH.TimecodeClass import *
from tkinter import *

# initialize hyperdeck list
hyperdecks = []
# initialize replay List
replays = []

# record_start_time
global record_start_time
record_start_time = 0
global recording
recording = False


# <editor-fold desc="Function definitions">
# define util functions
def add_log(string):
    main_log.append(string)


def print_log_total():
    for entry in main_log:
        print(entry)
        print("══════════════════════════")


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
        replays.append(Timecode(record_start_time+time()))  # TODO Test this to make sure it works


def recall_replay(timecode):
    print("DEBUG recalling replay "+timecode.get_hyperdeck_tc()+" on all Hyperdecks")
    for deck in hyperdecks:
        deck.goto(timecode)


def get_latest_time():
    for deck in hyperdecks:
        out = deck.send_command("clips get")
        last_clip = out[-32:-8]
        print(last_clip)

# </editor-fold>


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

start_recording()
sleep(10)
stop_recording()
get_latest_time()

root = Tk()  # Create GUI Window
replayNames = []

