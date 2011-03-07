from hw3hash import run as getHash


hashes = dict()

def recursiveGetHashes(s,l):
	"""hash all strings starting with s, of length less than l"""
	if len(s) >= l
		return
	hashes[s] = getHash(s)
	for i in xrange(255):
		recursiveGetHashes(s+chr(i),l)
	

recursiveGetHashes(chr(0),10)
