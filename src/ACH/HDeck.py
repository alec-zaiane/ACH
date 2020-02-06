import asyncio

import src.HyperDeck.HyperDeck as HDLibrary


class HDeck:
    def __init__(self, ip, name):
        self.Deck = HDLibrary.HyperDeck(ip)
        self.name = name
        self.ip = ip

    def connect(self):
        print("Connecting to "+self.ip)
        asyncio.run(self.Deck.connect())
        print("Connection Attempt Finished")
        # TODO replace debug code here with something better after seeing what it actually returns

    def test_connection(self):
        print("Testing Connection to "+self.ip)
        print("Ping returned: "+str(self.Deck.connected()))
        # TODO replace debug code with something better
