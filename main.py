import time
import sys
import os

from decompression import HuffmanDeCompressor
from compression import HuffmanCompressor

def main():
    value = input('(0) To Exit:\n(1) Compress File:\n(2) Decompress File:\n')
    startTime = time.time()
    if value == '1':
        encoder = HuffmanCompressor()
        name = input('Enter Location: ')
        encoder.compress(name)
        print("Time Elapsed: %s seconds" % (time.time() - startTime)+"\n")
    elif value == '2':
        decompressor = HuffmanDeCompressor()
        name = input('Enter Location: ')
        fileName = os.path.splitext(name)
        extension = fileName[1]
        if extension == '.dp':
            decompressor.decompress(name)
            print("Time Elapsed: %s seconds" % (time.time() - startTime)+"\n")
        else:
            print('File can\'t be decompressed before compressing')
    elif value == '0':
        sys.exit("Program Terminated...")

while True:
    main()
