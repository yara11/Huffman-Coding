# Python libs
from queue import PriorityQueue
import math
import timeit

# Local imports
from Node import Node

def calc_frequency(c, frequencies):
    if c in frequencies:
        frequencies[c] += 1
        return
    frequencies.update({c: 1})


def read_file(filename, binary):
    frequencies = {}
    mode = "rb" if binary else "r"
    with open(filename, mode) as f:
        while True:
            c = f.read(1)
            if not c:
                break
            calc_frequency(c, frequencies)
        f.close();
    return frequencies


def init_pq(frequencies):
    pq = PriorityQueue()
    for c, f in frequencies.items():
        pq.put(Node(f, c))
    
    return pq


def calculate_length(frequencies):
    global actual_length
    actual_length = 0
    for i in frequencies.keys():
        actual_length += (8*int(frequencies[i]))


def Huffman(frequencies):
    calculate_length(frequencies)
    pq = init_pq(frequencies)
    n = len(frequencies)
    for i in range(1, n):
        z = Node()
        z.left = pq.get()
        z.right = pq.get()
        z.freq = z.left.freq + z.right.freq
        pq.put(z)
    return pq.get()


encode = {}
decode = {}


def get_codes(frequencies, node = None, code = ""):
    if node is None:
        root = Huffman(frequencies)
        global compressed_length, map_size
        compressed_length=0
        map_size=0
        return get_codes(frequencies, root)

    if node.left is None and node.right is None:
        compressed_length+=(frequencies[node.char]*len(code))
        map_size+=5+(math.ceil(len(code)/8))
        encode[node.char] = code
        decode[code] = node.char

    if node.left:
        get_codes(frequencies, node.left, code+"0")

    if node.right:
        get_codes(frequencies, node.right, code+"1")


def write_header(f2):
    f2.write(compressed_length.to_bytes(4, 'little'))
    f2.write(map_size.to_bytes(4, 'little'))
    for i in encode:
        f2.write(ord(i).to_bytes(1, 'little'))
        f2.write(len(encode[i]).to_bytes(4, 'little'))
        f2.write(int(encode[i], 2).to_bytes(math.ceil(len(encode[i]) / 8), 'little'))


def write_compressed_code(f,f2):
    str=""
    while True:
        c = f.read(1)
        if not c:
            while (len(str) < 8):
                str += "0"
            f2.write(int(str, 2).to_bytes(1, 'little'))
            break
        x = encode[c]
        if (len(x) < 8 - len(str)):
            str += x
        else:
            while len(str) < 8 and len(x) != 0:
                str += x[0]
                x = x[1:]
                if len(str) == 8:
                    f2.write(int(str, 2).to_bytes(1, 'little'))
                    str = ""


def write_compressed_file(filename, binary):
    newfile = "compressed_" + filename
    with open(newfile, 'wb') as f2:
        write_header(f2)
        mode = "rb" if binary else "r"
        with open(filename, mode) as f:
            write_compressed_code(f,f2)
            f.close()
        f2.close()




def read_header(f):
    code_size = int.from_bytes(f.read(4), 'little')
    map_size = int.from_bytes(f.read(4), 'little')
    while map_size != 0:
        char = chr(int.from_bytes(f.read(1), 'little'))
        map_size -= 1
        char_size = int.from_bytes(f.read(4), 'little')
        map_size -= 4
        code = format(int.from_bytes(f.read(math.ceil(char_size / 8)), 'little'), '016b')
        map_size -= math.ceil(char_size / 8)
        decode[code[-char_size:]] = char
    return code_size


def write_decompressed_file_from_binary(f, f2, code_size):
	temp=""
	byte=8
	print(decode)
	while code_size != 0:
		c = f.read(1)
		code_size -= byte
		if not c:
		    break
		s = int.from_bytes(c, 'little')
		e = format(s, '08b')
		if code_size < 0:
		    e = e[:code_size]
		    byte = byte + 1 + code_size
		if code_size == 0:
		    byte += 1
		for i in range(0, byte):
		    if temp not in decode.keys():
		        temp += e[i]
		    else:
		        f2.write(decode[temp].encode('utf-8'))
		        if code_size > 0 or i + 1 != byte:
		            temp = e[i]

def write_decompressed_file(f,f2,code_size):
    temp=""
    byte=8
    while code_size != 0:
        c = f.read(1)
        code_size -= byte
        if not c:
            break
        s = int.from_bytes(c, 'little')
        e = format(s, '08b')
        if code_size < 0:
            e = e[:code_size]
            byte = byte + 1 + code_size
        if code_size == 0:
            byte += 1
        for i in range(0, byte):
            if temp not in decode.keys():
                temp += e[i]
            else:
                f2.write(decode[temp])
                if code_size > 0 or i + 1 != byte:
                    temp = e[i]

def calculate_ratio():
    print("Compressed ratio: %.2f" % (compressed_length/actual_length))


def compress(filename, binary):
	frequencies = read_file(filename, binary)
	get_codes(frequencies)
	write_compressed_file(filename, binary)
	calculate_ratio()

def decompress(filename, binary):
	with open(filename,'rb') as f:
		mode = "wb" if binary else "w"
		with open("decompressed_" + filename, mode) as f2:
			code_size = read_header(f)
			if binary:
				write_decompressed_file_from_binary(f, f2, code_size)
			else:
				write_decompressed_file(f, f2, code_size)


def run_and_return_time_elapsed(method, **kwargs):
	start = timeit.default_timer()
	method(kwargs['name'], kwargs['binary'])
	end = timeit.default_timer()
	return end - start

# read input and count occurences
name = input("Please enter filename: ")
option = input("Do you want to 1.compress or 2.decompress (1/2)? ")
binary = input ("Is it a binary file (y/n)?") == 'y'

if option == "1":
	print("Time elapsed: %.2f" % run_and_return_time_elapsed(compress, binary=binary, name=name))

elif option == "2":
    print("Time elapsed: %.2f" % run_and_return_time_elapsed(decompress, binary=binary, name=name))