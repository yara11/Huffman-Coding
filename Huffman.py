import sys
from queue import PriorityQueue

class Node:
    def __init__(self, freq = 0, char = '\0'):
        self.freq = freq
        self.char = char
        self.left = None
        self.right = None

    def __lt__(self, other):
        if self.freq != other.freq:
            return self.freq < other.freq
        return self.char < other.char


def calc_frequency(c, frequencies):
    if c in frequencies:
        frequencies[c] += 1
        return
    frequencies.update({c: 1})


def read_file(filename):
    frequencies = {}
    with open(filename[:-1]) as f:
        while True:
            c = f.read(1)
            if not c:
                break
            calc_frequency(c, frequencies)

    # print(frequencies)
    
    return frequencies

def init_pq(frequencies):
    pq = PriorityQueue()
    for c, f in frequencies.items():
        pq.put(Node(f, c))

    # while not pq.empty():
    #     i = pq.get()
    #     print(i.freq, " ", i.char)
    
    return pq

def Huffman(filename):
    frequencies = read_file(name)
    pq = init_pq(frequencies)
    n = len(frequencies)
    for i in range(1, n):
        z =  Node()
        z.left = pq.get()
        z.right = pq.get()
        z.freq = z.left.freq + z.right.freq
        pq.put(z)
    return pq.get()

encode = {}
decode = {}

def get_codes(filename, node = None, code = ""):
    if node is None:
        root = Huffman(filename)
        return get_codes(filename, root)

    if node.left is None and node.right is None:
        encode[node.char] = code
        decode[code] = node.char

    if node.left:
        get_codes(filename, node.left, code+"0")

    if node.right:
        get_codes(filename, node.right, code+"1")


# read input and count occurences
print("Please enter filename:")
name = sys.stdin.readline()

get_codes(name)
print(encode)
print(decode)
