

class replay:
    def __init__(self,clipindex,timecode):
        self.clipIndex = clipindex
        self.timeCode = timecode

    def getTime(self):
        return self.timeCode

    def getIndex(self):
        return self.clipIndex
