

class Replay:
    def __init__(self, clipindex, timecode):
        self.time_code = timecode
        self.stars = 0
        self.player = ""
        self.team = ""

    def get_time(self):
        return self.time_code


