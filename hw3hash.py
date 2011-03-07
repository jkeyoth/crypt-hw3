#!/usr/bin/python

import sys

#for testing
Sbox = [[64, 40, 694, 985, 157, 56, 868, 451, 944, 549, 481, 945, 680, 524, 261], [202, 816, 425, 490, 80, 948, 359, 530, 693, 191, 488, 685, 365, 445, 682], [936, 778, 377, 748, 648, 421, 267, 366, 892, 444, 900, 504, 664, 755, 221], [269, 190, 684, 927, 504, 880, 73, 595, 539, 52, 948, 214, 657, 228, 918], [42, 815, 820, 356, 511, 324, 438, 530, 556, 313, 822, 446, 559, 955, 690], [150, 128, 198, 13, 361, 650, 980, 363, 89, 478, 560, 132, 722, 269, 949], [169, 256, 99, 525, 726, 395, 982, 795, 673, 114, 419, 977, 19, 234, 787], [755, 701, 288, 262, 392, 212, 572, 274, 559, 102, 844, 847, 340, 428, 343], [506, 306, 804, 298, 870, 640, 53, 318, 349, 94, 931, 550, 928, 357, 585], [749, 49, 199, 963, 45, 429, 917, 203, 320, 988, 528, 670, 561, 789, 456], [949, 69, 475, 638, 567, 707, 353, 560, 874, 547, 779, 749, 208, 617, 151], [485, 954, 510, 135, 140, 846, 242, 424, 910, 90, 656, 380, 917, 378, 233], [854, 297, 224, 607, 218, 276, 861, 132, 44, 955, 263, 235, 267, 505, 539], [813, 54, 125, 475, 278, 356, 144, 761, 320, 723, 294, 769, 264, 791, 106], [565, 470, 587, 831, 43, 916, 400, 586, 671, 978, 472, 301, 404, 728, 677]]

smallBlocks = True
verbose = False

def splitPlainToBlocks(plain, blockSize):
	"""Split the plaintext into blocks"""
	charblocks = []
	for i in xrange(0,len(plain),blockSize):
		charblocks.append(plain[i:i+blockSize])
	if len(plain) % blockSize != 0:
		charblocks[-1] += plain[0:blockSize -len(charblocks[-1])]
	
	
	print charblocks, blockSize
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
	while len(z) < 8:
		z = "0" + z
	
	splitSpot = (len(z) / 4)# % len(Sbox)
	
	#get indexes for Sbox
	i = int(z[:splitSpot],2)
	j = int(z[splitSpot:],2)
	
	if verbose: print "Input:",len(plainText) * 8,"bits"
	return Sbox[i%len(Sbox)][j%len(Sbox[0])]# % (pow(2,len(plainText)))
	
	
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
	run(arg)
