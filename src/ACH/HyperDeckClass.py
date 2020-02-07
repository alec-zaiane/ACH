from telnetlib import Telnet
from src.ACH.ACH import *
import sys
from multiprocessing import Process
from time import sleep

tcp_port = 9993


class HyperDeck:

    def __init__(self, ip):
        self.ip = ip
        self.tn = Telnet(self.ip, tcp_port)
        self.log = []

    def add_log(self, to_log):
        self.log.append(to_log)
        main_log.append(self.ip+" | "+to_log)

    def print_log(self):
        for entry in self.log:
            print(entry)
            print("══════════════════════════")

    def send_command(self, command):
        print("send: " + command)
        add_log("send: "+command)
        tn = Telnet(self.ip, tcp_port)
        tn.write(bytes(command, "utf-8") + b'\r\n')
        # tn.write(b'quit'+b'\r\n') TODO determine if this is needed
        self.log.append(tn.read_all().decode('ascii'))
        main_log.append(self.log[-1])
        return self.log[-1]

    def send_user_command(self):
        command = input("Please type a command to send\n")
        print("Sending '"+command+"' to " + self.ip)
        print(self.send_command(command))

    def test_connection(self):
        add_log("pinging")
        print(self.send_command('ping'))

    # speed is int, loop and single_clip are boolean
    def play_specific(self, speed, loop, single_clip):
        proper_speed = max(min(speed, 1600), -1600)
        print("setting speed to "+proper_speed+" options: loop: "+loop+" single_clip: "+single_clip)
        add_log("set speed "+proper_speed+" options: loop: "+loop+" single_clip "+single_clip)
        self.send_command("play: speed: "+proper_speed+" loop: "+loop+" single clip: "+single_clip)

    def play(self, speed):
        proper_speed = max(min(speed, 1600), -1600)
        print("setting speed to " + proper_speed)
        add_log("set speed " + proper_speed)
        self.send_command("play: speed: "+proper_speed)


