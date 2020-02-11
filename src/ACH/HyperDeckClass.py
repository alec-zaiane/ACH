from telnetlib import Telnet
from threading import Thread
import socket

# initialize log
main_log = []

tcp_port = 9993
multithread = False  # Currently not working


class HyperDeck:

    def __init__(self, ip):
        self.ip = ip
        # self.tn = Telnet(self.ip, tcp_port)
        self.log = []
        self.always_print_log = False
        self.connectable = True

    def __str__(self):
        return "Hyperdeck @" + self.ip

    def add_log(self, to_log):
        self.log.append(to_log)
        main_log.append(self.ip + " | " + to_log)
        if self.always_print_log:
            print(self.ip + " | " + to_log)

    def print_log(self):
        # iterate over this object's log and print each element, separated by a horizontal line
        for entry in self.log:
            print(entry)
            print("══════════════════════════")
        # print out number of log entries
        print(str(len(self.log)) + " entries in HD @" + self.ip)

    def always_print_log(self, print_on_log_entry):
        self.always_print_log = print_on_log_entry

    def send_command(self, command):
        if self.connectable:
            self.add_log("send: " + command)
            if multithread:
                # open new thread with the goal of running send_command_multithread_process
                p1 = Thread(target=self.send_command_multithread_process, args=command)
                p1.start()  # run the thread
            else:
                try:
                    tn = Telnet(self.ip, tcp_port, timeout=4)  # Opens new telnet object with connection to Hyperdeck
                except (socket.timeout, TimeoutError):
                    self.connectable = False
                    self.add_log("TimeoutError, Hyperdeck refused to connect")
                    return "Error"
                tn.write(bytes(command, "utf-8") + b'\r\n')  # Sends the command to the Hyperdeck
                tn.write(b'quit' + b'\r\n')  # quit connection, for some reason this is needed
                out = tn.read_all().decode('ascii')  # Reads the hyperdeck's answer and writes it to a var
                self.add_log(out)  # adds the output to the log
                return out  # Return the hyperdeck's answer in case needed
        else:
            print(str(self) + " is not connected/not reachable, run test_connection() to verify and attempt to reconnect")
            return "Error: Hyperdeck is not connected"

    def send_command_multithread_process(self, command):
        tn = Telnet(self.ip, tcp_port)
        tn.write(bytes(command, "utf-8") + b'\r\n')
        tn.write(b'quit' + b'\r\n')
        out = tn.read_all().decode('ascii')
        self.add_log(out)
        # return statement kills the thread
        # since memory space is shared we don't have to worry about waiting for it and joining vars
        return out

    def send_user_command(self):
        command = input("Please type a command to send\n")
        print("Sending '" + command + "' to " + self.ip)
        print(self.send_command(command))

    def test_connection(self):
        self.connectable = True
        back = self.send_command('ping')
        return back

    def play_specific(self, speed, loop, single_clip):
        # speed is int, loop and single_clip are boolean
        proper_speed = str(max(min(speed, 1600), -1600))
        self.send_command("play: speed: " + proper_speed + " loop: " + loop + " single clip: " + single_clip)

    def play(self, speed):
        proper_speed = str(max(min(speed, 1600), -1600))
        self.send_command("play: speed: " + proper_speed)

    def record(self):
        self.send_command("record")

    def stop(self):
        self.send_command("stop")

    def goto(self, timecode):
        # TODO Verify timecode format before sending message
        self.send_command("jog: timecode:" + timecode)

    def get_clips(self):
        self.send_command("clips get")
        # TODO convert to list of clips
        clips_start_times = []
        clips_end_times = []

        # Groups clip start and end into a 2d list
        clips = [clips_start_times, clips_end_times]
        return clips
