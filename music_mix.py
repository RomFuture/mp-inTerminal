class ML:
    def __init__(self):
        self.index = 0
    def next_track(self):
        self.index += 1
        return self.index
    def last_track(self):
        self.index -= 1
        return self.index