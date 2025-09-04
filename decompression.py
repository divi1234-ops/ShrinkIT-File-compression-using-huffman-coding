from node import Node

class HuffmanDeCompressor:
    def __init__(self):
        self.fileName = ''
        self.fileExtension = ''

    def decompress(self, inputFileName: str):
        self.fileName = inputFileName.split('.')[0]
        self.fileExtension = inputFileName.split('.')[1]
        outputFileName = f"{self.fileName}.{self.fileExtension}"
        fileBytes: str = self.readFile(inputFileName)
        decodedBytes: list = self.decode(fileBytes)
        self.save(outputFileName, decodedBytes)

    def readFile(self, inputFileName: str):
        inputFile = open(inputFileName, "rb")
        encodedBytes = ""
        byte = inputFile.read(1)
        while len(byte) > 0:
            encodedBytes += f"{bin(ord(byte))[2:]:0>8}"
            byte = inputFile.read(1)
        return encodedBytes

    def decode(self, encodedBytes: str):
        bitsStream = list(encodedBytes)
        tree = self.decodeTree(bitsStream)
        reversedLookupTable = self.buildReversedLookupTable(tree)
        bitsStream = self.removePadding(bitsStream)
        encodedBytes = ''.join(bitsStream)
        outputBytes = []
        byteKey = ''
        for bit in encodedBytes:
            byteKey += bit
            byteValue = reversedLookupTable.get(byteKey)
            if byteValue is not None:
                outputBytes.append(byteValue)
                byteKey = ''
        return outputBytes

    def decodeTree(self, bitsStream):
        bit = bitsStream[0]
        del bitsStream[0]
        if bit == "1":
            byte = ""
            for _ in range(8):
                byte += bitsStream[0]
                del bitsStream[0]
            return Node(int(byte, 2))
        else:
            left = self.decodeTree(bitsStream)
            right = self.decodeTree(bitsStream)
            return Node(None, left=left, right=right)

    def removePadding(self, bitsStream):
        numOfZeros_Bin = bitsStream[:8]
        numOfZeros_Int = int("".join(numOfZeros_Bin), 2)
        bitsStream = bitsStream[8:]
        bitsStream = bitsStream[numOfZeros_Int:]
        return bitsStream

    def buildReversedLookupTable(self, huffmanTree: Node):
        lookupTable = {}
        self.buildReversedLookupTableImpl(huffmanTree, "", lookupTable)
        if len(lookupTable) == 1:
            key = next(iter(lookupTable))
            lookupTable[key] = '1'
        return {v: k for k, v in lookupTable.items()}

    def buildReversedLookupTableImpl(self, node: Node, code, lookupTable):
        if node.isLeaf():
            lookupTable[node.byte] = code
        else:
            self.buildReversedLookupTableImpl(node.left, code + "0", lookupTable)
            self.buildReversedLookupTableImpl(node.right, code + "1", lookupTable)

    def save(self, outputFileName: str, outputBytesNum):
        outputBytes = ''
        for num in outputBytesNum:
            outputBytes += format(num, '08b')
        b_arr = bytearray()
        for i in range(0, len(outputBytes), 8):
            b_arr.append(int(outputBytes[i:i + 8], 2))
        outputFile = open(f"OG{outputFileName}", "wb")
        outputFile.write(b_arr)
