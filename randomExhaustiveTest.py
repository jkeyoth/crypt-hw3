#!/usr/bin/python

import sys
import os
import random
import string

startLength = int(sys.argv[1])
endLength = int(sys.argv[2])
numTries = int(sys.argv[3])
plainLength = int(sys.argv[4])

random.seed()

paraIn = open("paraIn.txt","w")

pullFrom = string.letters + string.digits + string.punctuation

for i in xrange(numTries):
	plain = ""
	for j in xrange(plainLength):
		plain += random.choice(pullFrom)
		
	paraIn.write(str(startLength) + "\n" + str(endLength) + "\n" + plain + "\n")

paraIn.close()

os.system("./runExhaustive.sh > exhaustiveOutput")

outputIn = open("exhaustiveOutput")

tries = []

for l in outputIn:
	tries.append(int(l))

sums = 0
csums = 0
noFounds = 0
for t in tries:
	sums += t
	if t == endLength:
		noFounds += 1
	else:
		csums += t

print "Found colision",numTries-noFounds,"times out of",numTries,"runs of exhaustive search"
print "Average number of tries when colision found:",csums/(numTries-noFounds)
print "Average number of tries over all",numTries,"runs:",sums/numTries


