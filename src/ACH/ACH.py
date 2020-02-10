from src.ACH.HyperDeckClass import*
import os
from multiprocessing import Process

# initialize hyperdeck list
hyperdecks = []


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


