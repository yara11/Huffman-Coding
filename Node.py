class Node:
    def __init__(self, freq = 0, char = '\0'):
        self.freq = freq
        self.char = char
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq or (self.freq == other.freq and str(self.char) < str(other.char))
