#!/usr/bin/python

import sys, random

"""Generate a python array to use as an Sbox. Output can be copied to code"""


if len(sys.argv) < 3:
	print "Usage: genSBox.py numRows numCols"
	exit(1)

numRows = int(sys.argv[1])
numCols = int(sys.argv[2])

seed = 0

if len(sys.argv) > 3:
	seed = int(sys.argv[3])

random.seed(seed if seed!=0 else None)

sbox = []
for i in xrange(numRows):
	sbox.append(random.sample(xrange(10000),numCols))

print sbox
		
		

