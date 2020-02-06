

class replay:
    def __init__(self,clipindex,timecode):
        self.clipIndex = clipindex
        self.timeCode = timecode

    def gettime(self):
        return self.timeCode

    def getindex(self):
        return self.clipIndex
