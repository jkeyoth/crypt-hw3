#!/usr/bin/python

import sys

#for testing
Sbox = [[8112, 9085, 7791, 9840, 901, 9530, 43, 9107, 5216, 6048, 9361, 9764], [2106, 2145, 434, 3280, 2465, 6108, 6619, 4900, 6995, 9378, 3379, 4888], [7608, 5882, 6982, 6999, 9067, 9398, 4767, 6639, 8723, 5878, 5752, 3097], [8399, 7752, 2936, 1548, 49, 3098, 3279, 718, 1240, 4816, 9265, 6073], [4557, 824, 1680, 515, 3601, 9593, 736, 9717, 2396, 4323, 6327, 6252], [1819, 4124, 6721, 5653, 8318, 9243, 9543, 7704, 6689, 753, 8095, 739], [7434, 1722, 9281, 4184, 5020, 5203, 6721, 9947, 6341, 343, 3971, 4649], [7624, 8150, 5225, 4973, 9180, 8928, 2960, 6188, 2555, 6407, 7782, 3290], [5758, 3343, 4438, 7969, 2484, 1988, 5478, 399, 8331, 3292, 6598, 2988], [9989, 6260, 5478, 3816, 9648, 7013, 8203, 4456, 161, 9183, 1705, 1340], [550, 6402, 5706, 5513, 75, 9751, 558, 8927, 7450, 500, 6618, 4341], [9046, 4133, 9781, 930, 4891, 2937, 8855, 1060, 7807, 5404, 6373, 8327]]
smallBlocks = True
verbose = False

def splitPlainToBlocks(plain, blockSize):
	"""Split the plaintext into blocks"""
	charblocks = []
	for i in xrange(0,len(plain),blockSize):
		charblocks.append(plain[i:i+blockSize])
	if len(plain) % blockSize != 0:
		charblocks[-1] += plain[0:blockSize -len(charblocks[-1])]
	
	
	blocks = []	#blocks is a 2d array
	
	for i in xrange(len(charblocks)):
		blocks.append([])
		s = charblocks[i]
		for c in s:
			blocks[i].append(ord(c))
	
	return blocks

def splitPlainToSmallBlocks(plain, blockSize):
	if blockSize != 2 and blockSize != 4:
		print "Bad small block size"
		exit(-1)
	
	blocks = []
	
	if blockSize == 4:
		for c in plain:
			o = ord(c)
			blocks.append(o>>4)
			blocks.append(o%16)
	
	else:#2 bit blocks
		temp = []
		for c in plain:
			o = ord(c)
			for i in xrange(4):
				temp.append(o%4)
				o /= 4
			for i in xrange(3,-1,-1):
				blocks.append(temp[i])
			
		
	
	return blocks
	
	

def paritySmall(block):
	runTot = block
	#2 bits
	firstHalf = runTot >> 2
	secondHalf = runTot % 4
	runTot = runTot = firstHalf ^ secondHalf
	
	#parity bit
	firstHalf = runTot >> 1
	secondHalf = runTot % 2
	return firstHalf ^ secondHalf

def parity(block):
	"""return the parity as an int"""
	#reduce block to 8 bits
	runTot = block[0]
	for i in xrange(1,len(block)):
		runTot = runTot ^ block[i]
	
	#reduce runTot to 4 bits
	firstHalf = runTot >> 4
	secondHalf = runTot % 16
	runTot = firstHalf ^ secondHalf
	
	#2 bits
	firstHalf = runTot >> 2
	secondHalf = runTot % 4
	runTot = runTot = firstHalf ^ secondHalf
	
	#parity bit
	firstHalf = runTot >> 1
	secondHalf = runTot % 2
	return firstHalf ^ secondHalf



def keylessHash(plainText):
	"""Driver function for hashing"""
	if smallBlocks:
		blocks = splitPlainToSmallBlocks(plainText, 2)	#blocks of 2 or 4 bits
	else:
		blocks = splitPlainToBlocks(plainText, 2)	#blocks of one or more characters
	
	#print blocks
	
	#build parity string z
	z = ""
	for block in blocks:
		z += str(paritySmall(block)) if smallBlocks else str(parity(block))
	
	#add leading zeros
	while len(z) < 4:
		z = "0" + z
	
	splitSpot = (len(z) / 2)# % len(Sbox)
	
	#get indexes for Sbox
	i = int(z[:splitSpot],2) % len(Sbox)
	j = int(z[splitSpot:],2) % len(Sbox[0])
	
	
	if verbose: print "Input:",len(plainText) * 8,"bits"
	return Sbox[i][j]# % (pow(2,len(plainText)))
	
	
def run(plain, mained = False):
	

	hashed = keylessHash(plain)

	if verbose: print "Decimal:\t",hashed
	if verbose: print "Binary:\t\t",bin(hashed)[2:]
	if verbose:
		print "Hex:\t\t",hex(hashed)
	elif mained:
		print hex(hashed)
	return hashed
	
if __name__ == "__main__":
	arg = ""
	for i in xrange(1,len(sys.argv)):
		arg += sys.argv[i]
	run(arg, true)
