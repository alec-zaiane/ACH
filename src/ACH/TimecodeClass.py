class Timecode:
    def __init__(self, time, milli=True):
        self.millis = time
        # HyperDeck timecode is in HH:MM:SS:FF

    def set_now(self, start_time):
        # sets to the
        return

    def to_hyperdeck_code(self):
        total_frames = self.millis*1000/60
        frames = total_frames % 60
        total_frames -= frames
        remaining_seconds = total_frames/60
        seconds = remaining_seconds % 60
        remaining_seconds -= seconds
        remaining_minutes = remaining_seconds/60
        minutes = remaining_minutes % 60
        remaining_minutes -= minutes
        hours = remaining_minutes/60
        return str(hours)+":"+str(minutes)+":"+str(seconds)+":"+str(frames)
