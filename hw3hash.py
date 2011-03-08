#!/usr/bin/python

import sys

#for testing
Sbox = [[8950, 5044, 7307, 1264, 40, 9334, 3551, 2962, 5556, 5077, 2972, 1937, 685, 746, 1946, 655], [6836, 127, 3884, 4788, 8908, 9203, 680, 2374, 8782, 7956, 6193, 7481, 4875, 6705, 3119, 8773], [6495, 2528, 1802, 115, 1581, 8702, 1635, 6193, 267, 5722, 7357, 7970, 7410, 7732, 7716, 5585], [7696, 6790, 4254, 5379, 6996, 3729, 6975, 9021, 2268, 4190, 5285, 6379, 4441, 1219, 8355, 4309], [8586, 6872, 3453, 9332, 5486, 7800, 7527, 9949, 8023, 7243, 6268, 786, 1066, 4758, 6821, 1505], [8233, 1188, 26, 5285, 1607, 425, 5475, 8810, 1732, 4083, 309, 8705, 8801, 3689, 1575, 2329], [631, 2135, 3386, 6465, 7812, 8938, 5169, 1992, 929, 981, 1721, 6380, 2375, 5885, 8666, 9584], [1006, 5658, 946, 4431, 51, 525, 434, 6541, 7585, 8799, 576, 2959, 299, 1168, 7203, 5891], [2317, 5536, 4634, 5194, 2591, 7624, 9623, 8615, 194, 774, 3608, 864, 6345, 9560, 6463, 6487], [4708, 2338, 3223, 7948, 6462, 8110, 923, 8716, 2112, 8493, 4304, 101, 4648, 1016, 1553, 8227], [5767, 7993, 9868, 137, 7706, 4814, 2100, 6826, 2651, 5404, 1709, 184, 1109, 5780, 2248, 8105], [7665, 1986, 5942, 1385, 1837, 7208, 1973, 8021, 6189, 6318, 8265, 1989, 4159, 1044, 9652, 9189], [5844, 6714, 5770, 4338, 3397, 5205, 8102, 2935, 8881, 7680, 9097, 5097, 9752, 2280, 1144, 6317], [7178, 3252, 2689, 6202, 1833, 2957, 8038, 4696, 5157, 4115, 1452, 9105, 6979, 8875, 3982, 1807], [9453, 6390, 3178, 7968, 1573, 1754, 2114, 5428, 4918, 5603, 4750, 1379, 4027, 6662, 3007, 2762], [9080, 5876, 6448, 4231, 4127, 809, 7559, 1854, 3888, 7143, 937, 7523, 7569, 109, 6526, 6863]]
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
	print len(Sbox), len(Sbox[0])
	arg = ""
	for i in xrange(1,len(sys.argv)):
		arg += sys.argv[i]
	run(arg, True)
