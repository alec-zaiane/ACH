

class Replay:
    def __init__(self, clipindex, timecode):
        self.clipIndex = clipindex
        self.timeCode = timecode

    def get_time(self):
        return self.timeCode

    def get_index(self):
        return self.clipIndex
