import src.HyperDeck.HyperDeck as HDLibrary


class HDeck:
    def __init__(self, ip, name):
        self.Deck = HDLibrary.HyperDeck(ip)
        self.name = name
        self.ip = ip

    def connect(self):
        print("Connecting to "+self.ip)
        print("Connection returned: "+self.Deck.connect())
        # TODO replace debug code here with something better after seeing what it actually returns

    def testConnection(self):
        print("Testing Connection to "+self.ip)
        print("Ping returned: "+self.Deck.connected())
        # TODO replace debug code with something better
