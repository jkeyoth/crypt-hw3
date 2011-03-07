#!/usr/bin/python
from hw3hash import run as getHash
import sys, math

if len(sys.argv) < 4:
	print "Usage: exhaustive startLength endLength stringToHash"

hashToFind = getHash(sys.argv[3])

startNum = int(sys.argv[1])
endNum = int(sys.argv[2])

#startNum = pow(2,startNum*8)
#endNum = pow(2,endNum*8)

print "Doing",startNum,"to",endNum
tries = 0
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
		print "colision found after",tries,"tries"
		exit(0)
	tries += 1
	if i%100000 == 0:
		print float(i)/endNum * 100,"%"

print "No colision found"
