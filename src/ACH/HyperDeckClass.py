from telnetlib import Telnet
from src.ACH.ACH import *
from multiprocessing import Process

tcp_port = 9993
multithread = False


class HyperDeck:

    def __init__(self, ip):
        self.ip = ip
        self.tn = Telnet(self.ip, tcp_port)
        self.log = []
        self.always_print_log = False

    def add_log(self, to_log):
        self.log.append(to_log)
        main_log.append(self.ip+" | "+to_log)
        if self.always_print_log:
            print(self.ip+" | "+to_log)

    def print_log(self):
        for entry in self.log:
            print(entry)
            print("══════════════════════════")
        print(str(len(self.log))+" entries in HD @"+self.ip)

    def always_print_log(self, print_on_log_entry):
        self.always_print_log = print_on_log_entry

    def send_command(self, command):
        print("send: " + command)
        add_log("send: "+command)
        if multithread:
            p1 = Process(target=self.send_command_multithread_process, args=command)
            p1.start()
        else:
            tn = Telnet(self.ip, tcp_port)
            tn.write(bytes(command, "utf-8") + b'\r\n')
            # tn.write(b'quit'+b'\r\n') TODO determine if this is needed
            add_log(tn.read_all().decode('ascii'))
            return self.log[-1]

    def send_command_multithread_process(self, command):
        tn = Telnet(self.ip,tcp_port)
        tn.write(bytes(command, "utf-8") + b'\r\n')
        # tn.write(b'quit'+b'\r\n') TODO determine if this is needed
        out = tn.read_all().decode('ascii')
        add_log(out)
        return out

    def send_user_command(self):
        command = input("Please type a command to send\n")
        print("Sending '"+command+"' to " + self.ip)
        print(self.send_command(command))

    def test_connection(self):
        add_log("pinging")
        self.send_command('ping')

    def play_specific(self, speed, loop, single_clip):
        # speed is int, loop and single_clip are boolean
        proper_speed = str(max(min(speed, 1600), -1600))
        add_log("set speed "+proper_speed+" options: loop: "+loop+" single_clip "+single_clip)
        self.send_command("play: speed: "+proper_speed+" loop: "+loop+" single clip: "+single_clip)

    def play(self, speed):
        proper_speed = str(max(min(speed, 1600), -1600))
        add_log("set speed " + proper_speed)
        self.send_command("play: speed: "+proper_speed)

    def record(self):
        add_log("record")
        self.send_command("record")

    def stop(self):
        add_log("stopping")
        self.send_command("stop")
