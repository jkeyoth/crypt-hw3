#!/usr/bin/python
from hw3hash import run as getHash
import sys, math

hashes = dict()

start = int(sys.argv[1])
end = int(sys.argv[2])

startNum = pow(2,start*8)
endNum = pow(2,end*8)

for i in xrange(startNum, endNum):
	numCharsNow = int(math.log(i,2)) / 8 + 1
	plain = ""
	curVal = i
	for j in xrange(numCharsNow):
		c = curVal % 256
		plain = chr(c) + plain
		curVal = curVal >> 4
	hashes[plain] = getHash(plain)
	if i%100000 == 0:
		print float(i)/endNum * 100,"%"

print hashes
