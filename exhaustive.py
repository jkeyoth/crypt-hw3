#!/usr/bin/python
from hw3hash import run as getHash
import sys, math

verbose = False

if len(sys.argv) < 4:
	print "Usage: exhaustive startLength endLength stringToHash"

hashToFind = getHash(sys.argv[3])

startNum = int(sys.argv[1])
endNum = int(sys.argv[2])

#startNum = pow(2,startNum*8)
#endNum = pow(2,endNum*8)

if verbose: print "Doing",startNum,"to",endNum
tries = 1
for i in xrange(startNum, endNum):
	try:
		numCharsNow = int(math.log(i,2)) / 8 + 1
	except:
		continue
	plain = ""
	curVal = i
	for j in xrange(numCharsNow):
		c = curVal % 256
		plain = chr(c) + plain
		curVal = curVal >> 4
	if hashToFind == getHash(plain):
		if verbose:
			print "colision found after",tries,"tries"
		else:
			print tries
		exit(0)
	tries += 1
	if i%100000 == 0:
		if verbose: print float(i)/endNum * 100,"%"

if verbose:
	print "No colision found"
else:
	print tries
