from telnetlib import Telnet
from threading import Thread
import socket


# initialize log
main_log = []

tcp_port = 9993
multithread = False


class HyperDeck:

    def __init__(self, ip):
        self.ip = ip
        # self.tn = Telnet(self.ip, tcp_port)
        self.log = []
        self.error_log = []
        self.always_print_log = False
        self.connectable = True
        self.firstConnect = True
        self.send_command("play")
        self.mode = "play"
        self.send_command("stop")
        self.end_time = ""

    def __str__(self):
        return "Hyperdeck @" + self.ip

    def add_log(self, to_log, from_hd=False):
        if from_hd:
            # Scan to_log for the error codes
            return_code = to_log[0:3]
            if not (return_code == "200" or return_code == "500" or return_code == "205"):
                # There has been an error
                self.print_error_code(return_code)
                self.error_log.append(to_log)
        # Add to_log to the logs
        self.log.append(to_log)
        main_log.append(self.ip + " | " + to_log)
        if self.always_print_log:
            print(self.ip + " | " + to_log)
        return to_log

    def print_error_code(self, code):
        if code == "100":
            print(str(self)+"| 100 Syntax error")
        elif code == "101":
            print(str(self)+"| 101 unsupported parameter")
        elif code == "102":
            print(str(self)+"| 102 Invalid Value")
        elif code == "103":
            print(str(self)+"| 103 unsupported")
        elif code == "104":
            print(str(self)+"| 104 disk full")
        elif code == "105":
            print(str(self)+"| 105 no disk")
        elif code == "106":
            print(str(self)+"| 106 disk error")
        elif code == "107":
            print(str(self)+"| 107 timeline empty")
        elif code == "108":
            print(str(self)+"| 108 internal error")
        elif code == "109":
            print(str(self)+"| 109 out of range")
        elif code == "110":
            print(str(self)+"| 110 no input")
        elif code == "111":
            print(str(self)+"| 111 remote control disabled")
        elif code == "120":
            print(str(self)+"| 120 connection rejected")
        elif code == "150":
            print(str(self)+"| 150 invalid state")
        elif code == "151":
            print(str(self)+"| 151 invalid codec")
        elif code == "160":
            print(str(self)+"| 160 invalid format")
        elif code == "161":
            print(str(self)+"| 161 invalid token")
        elif code == "162":
            print(str(self)+"| 162 format not prepared")
        else:
            print(code+"| Unregistered Error")

    def print_log(self):
        # iterate over this object's log and print each element, separated by a horizontal line
        for entry in self.log:
            print(entry)
            print("══════════════════════════")
        # print out number of log entries
        print(str(len(self.log)) + " entries in HD @" + self.ip)

    def always_print_log(self, print_on_log_entry):
        self.always_print_log = print_on_log_entry

    def send_command(self, command, reply=True):
        if self.connectable:
            self.add_log("send: " + command)
            if multithread:
                print("DEBUG Command:" + command)
                # open new thread with the goal of running send_command_multithread_process
                p1 = Thread(target=self.send_command_multithread_process, args=(self, command))
                p1.start()  # run the thread
            else:
                try:
                    tn = Telnet(self.ip, tcp_port, timeout=4)  # Opens new telnet object with connection to Hyperdeck
                except (socket.timeout, TimeoutError):
                    self.connectable = False
                    self.add_log("TimeoutError, Hyperdeck refused to connect")
                    if not self.firstConnect:
                        print(str(self)+" Refused to connect")
                    self.firstConnect = False
                    return "Error"
                tn.write(bytes(command, "utf-8") + b'\r\n')  # Sends the command to the Hyperdeck
                tn.write(b'quit' + b'\r\n')  # quit connection, for some reason this is needed
                if reply:
                    out = tn.read_all().decode('ascii')  # Reads the hyperdeck's answer and writes it to a var
                else:
                    out = "200 reply disabled"
                self.add_log(out, from_hd=True)  # adds the output to the log
                return out  # Return the hyperdeck's answer in case needed
        else:
            print(str(self) + " is not connected/not reachable, run test_connection() to verify and attempt to reconnect")
            return "Error: Hyperdeck is not connected"

    def send_command_multithread_process(self, command):
        print("DEBUG Command inside multithread"+command)
        try:
            tn = Telnet(self.ip, tcp_port)
        except (socket.timeout, TimeoutError):
            self.connectable = False
            self.add_log("TimeoutError, Hyperdeck refused to connect")
            if not self.firstConnect:
                print(str(self) + " Refused to connect")
            self.firstConnect = False
            return "Error"
        tn.write(bytes(command, "utf-8") + b'\r\n')
        tn.write(b'quit' + b'\r\n')
        out = tn.read_all().decode('ascii')
        self.add_log(out, from_hd=True)
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
        self.mode = "play"

    def record(self):
        self.send_command("record")
        self.mode = "record"

    def stop(self):
        self.send_command("stop")

    def goto(self, timecode):
        # TODO Verify timecode format before sending message
        self.send_command("goto: timecode:" + timecode, reply=False )
        self.mode = "play"

    def get_clips(self):  # not sure if actually needed
        self.send_command("clips get")
        # TODO convert to list of clips
        clips_start_times = []
        clips_end_times = []

        # Groups clip start and end into a 2d list
        clips = [clips_start_times, clips_end_times]
        return clips
