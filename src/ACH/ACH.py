from HyperDeckClass import HyperDeck

Hd1 = HyperDeck("10.0.1.16")
Hd1.test_connection()

while True:
    Hd1.send_user_command()
