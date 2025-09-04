import os
from queue import PriorityQueue
from node import Node

class HuffmanCompressor:
    def __init__(self):
        self.fileName = ''
        self.queue = PriorityQueue()

    def compress(self, inputFileName: str):
        self.fileName = inputFileName
        bytesList = open(inputFileName, 'rb').read()
        frequencyTable = self.buildFrequencyTable(bytesList)
        huffmanTree = self.buildTree(frequencyTable)
        lookupTable = self.buildLookupTable(huffmanTree)
        encodedBytes = self.buildEncodedBytes(bytesList, lookupTable)
        self.save(huffmanTree, encodedBytes)
        self.CompressionRatio()

    def buildFrequencyTable(self, bytesList):
        bytesSet = set(bytesList)
        frequencyTable = {byte: 0 for byte in bytesSet}
        for byte in bytesList:
            frequencyTable[byte] += 1
        return frequencyTable

    def buildTree(self, frequencyTable):
        for byte, frequency in frequencyTable.items():
            self.queue.put(Node(byte, frequency))
        while self.queue.qsize() > 1:
            left, right = self.queue.get(), self.queue.get()
            parent = Node(None, left.freq + right.freq, left, right)
            self.queue.put(parent)
        return self.queue.get()

    def buildLookupTable(self, huffmanTree: Node):
        lookupTable = {}
        self.buildLookupTableImpl(huffmanTree, "", lookupTable)
        if len(lookupTable) == 1:
            key = next(iter(lookupTable))
            lookupTable[key] = '1'
        return lookupTable

    def buildLookupTableImpl(self, node: Node, code, lookupTable):
        if node.isLeaf():
            lookupTable[node.byte] = code
        else:
            self.buildLookupTableImpl(node.left, code + "0", lookupTable)
            self.buildLookupTableImpl(node.right, code + "1", lookupTable)

    def buildEncodedBytes(self, bytesList, lookupTable):
        encodedBytes = ""
        for byte in bytesList:
            encodedBytes += lookupTable[byte]
        return encodedBytes

    def encodeTree(self, node: Node, text):
        if node.isLeaf():
            text += "1"
            text += f"{node.byte:08b}"
        else:
            text += "0"
            text = self.encodeTree(node.left, text)
            text = self.encodeTree(node.right, text)
        return text

    def addPadding(self, encodedTree: str, encodedBytes: str):
        num = 8 - (len(encodedBytes) + len(encodedTree)) % 8
        if num != 0:
            encodedBytes = num * "0" + encodedBytes
        return f"{encodedTree}{num:08b}{encodedBytes}"

    def save(self, tree: Node, encodedBytes: str):
        encodedTree = self.encodeTree(tree, '')
        outputBytes = self.addPadding(encodedTree, encodedBytes)
        outputFile = open(self.fileName + '.dp', "wb")
        b_arr = bytearray()
        for i in range(0, len(outputBytes), 8):
            b_arr.append(int(outputBytes[i:i + 8], 2))
        outputFile.write(b_arr)

    def CompressionRatio(self):
        inputFileName = self.fileName
        outputFileName = self.fileName + '.dp'
        sizeBefore = os.path.getsize(inputFileName)
        sizeAfter = os.path.getsize(outputFileName)
        percent = round(100 - sizeAfter / sizeBefore * 100, 1)
        print(f"Before: {sizeBefore} bytes\nAfter: {sizeAfter} bytes\n"f"Compressed Percentage {percent}%")
