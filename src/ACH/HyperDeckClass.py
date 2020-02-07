from telnetlib import Telnet
import sys
from multiprocessing import Process


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
