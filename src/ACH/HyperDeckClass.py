from telnetlib import Telnet
import sys
from multiprocessing import Process
from time import sleep

tcp_port = 9993


class HyperDeck:

    def send_command(self, command):
        print("out: " + command)
        tn = Telnet(self.ip, tcp_port)
        tn.write(bytes(command, "utf-8") + b'\r\n')
        tn.write(b'quit'+b'\r\n')
        return tn.read_all().decode('ascii')

    def __init__(self, ip):
        self.ip = ip
        self.tn = Telnet(self.ip, tcp_port)

    def test_connection(self):
        print("Testing Connection to " + self.ip)
        print(self.send_command('ping'))

    def send_user_command(self):
        command = input("Please type a command to send\n")
        print("Sending '"+command+"' to " + self.ip)
        print(self.send_command(command))
