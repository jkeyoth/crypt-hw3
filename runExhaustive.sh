cat paraIn.txt | parallel -N3 ./exhaustive.py {1} {2} {3}

