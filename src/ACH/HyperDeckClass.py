from telnetlib import Telnet
import sys
from multiprocessing import Process


def send_command(tn, command):
    print("out: "+command)
    tn.write(bytes(command, "utf-8") + b'\r\n')
    return tn.read_all().decode('ascii')


class HyperDeck:

    def __init__(self, ip):
        self.ip = ip
        self.tcp_port = 9993

    def test_connection(self):
        print("Testing Connection to " + self.ip)
        tn = Telnet(self.ip, self.tcp_port)
        tn.write(b'ping' + b'\r\n')
        tn.write(b'quit' + b'\r\n')
        status = tn.read_all().decode('ascii')
        print(status)

    def send_user_command(self):
        command = input("Please type a command to send")
        print("Sending command to " + self.ip)
        tn = Telnet(self.ip, self.tcp_port)
        tn.write(bytes(command, "utf-8") + b'\r\n')
        tn.write(b'quit' + b'\r\n')
        status = tn.read_all().decode('ascii')
        print(status)
