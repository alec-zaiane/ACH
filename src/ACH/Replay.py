def check_code_string(string):
    # Makes sure input is 2 digits for the timecode
    if len(string) == 2:
        return string
    elif len(string) == 1:
        return "0"+string
    else:
        return string[:2]


def to_hyperdeck_code(millis):
    total_frames = round(millis/1000*60)
    frames = round(total_frames % 60)
    remaining_frames = total_frames-frames
    total_seconds = remaining_frames/60
    seconds = round(total_seconds % 60)
    remaining_seconds = total_seconds-seconds
    total_minutes = remaining_seconds/60
    minutes = round(total_minutes % 60)
    remaining_minutes = total_minutes-minutes
    hours = round(remaining_minutes/60)
    return check_code_string(str(hours))+":"+check_code_string(str(minutes))+":"+check_code_string(str(seconds))+";"+check_code_string(str(frames))


def to_millis(timecode):
    hours = timecode[:2]
    minutes = timecode[3:5]
    seconds = timecode[6:8]
    frames = timecode[9:]
    return round(int(frames)*16.6666667)+(int(seconds)*1000)+(int(minutes)*60000)+(int(hours)*3600000)


class Replay:
    def __init__(self, time, name):
        self.millis = time
        self.name = name
        # HyperDeck timecode is in HH:MM:SS;FF

    def set_now(self, start_time):
        # sets to the
        return

    def get_hyperdeck_tc(self):
        return to_hyperdeck_code(self.millis)

    def set_millis(self, milli):
        self.millis = milli
