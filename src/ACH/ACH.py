from src.ACH.HyperDeckClass import HyperDeck


# initialize hyperdeck list
hyperdecks = []
# initialize log
main_log = []


# define util functions
def add_log(string):
    main_log.append(string)


def print_log_total():
    for entry in main_log:
        print(entry)
        print("══════════════════════════")


Hd1 = HyperDeck("10.0.1.16")
Hd1.test_connection()

while True:
    Hd1.send_user_command()


