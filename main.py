import os
import glob
from Huffman import *
import zipfile

option = input("Do you want to 1.compress or 2.decompress (1/2)? ")

if input("1.Folder or 2.File (1/2)? ") == "1":
  directory = input ("Please enter folder name: ")
  if option == "1":
    os.makedirs('compressed_'+directory)
    for infile in glob.glob(os.path.join(directory, '*.*')):
      binary = input ("Is %s a binary file (y/n)? " % infile) == 'y'
      print("Time elapsed: %.2f" % run_and_return_time_elapsed(compress, binary=binary, name=str(infile)))

  elif option == "2":
    os.makedirs('decompressed_'+directory)
    for infile in glob.glob(os.path.join(directory, '*.*')):
      binary = input ("Is %s a binary file (y/n)? " % infile) == 'y'
      print("Time elapsed: %.2f" % run_and_return_time_elapsed(decompress, binary=binary, name=str(infile)))

else:
  # read input and count occurences
  name = input("Please enter file name: ")
  binary = input ("Is it a binary file (y/n)? ") == 'y'

  if option == "1":
    print("Time elapsed: %.2f" % run_and_return_time_elapsed(compress, binary=binary, name=name))

  elif option == "2":
    print("Time elapsed: %.2f" % run_and_return_time_elapsed(decompress, binary=binary, name=name))