import plac
import os
from collections import defaultdict
import logging

logging.basicConfig (format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

@plac.annotations(
	dirname = ("path of the directory", "positional"),
	srcfile = ("source filename", "positional"),
	tgtfile = ("target filename", "positional")
)
def main (dirname, srcfile, tgtfile):
	V = defaultdict (int)
	Vlower = defaultdict (int)
	VUPPER = defaultdict (int)
	VTitle = defaultdict (int)

	with open (os.path.join (dirname, srcfile)) as fin:
		for i, line in enumerate (fin):
			tokens = line.strip().split(" ")
			for token in tokens:
				if token.isalpha():
					lcaseToken = token.lower()
					V[lcaseToken] += 1
					Vlower[lcaseToken] += int (token.islower())
					VUPPER[lcaseToken] += int (token.isupper())
					VTitle[lcaseToken] += int (token.istitle())

			if (i+1) % 10000 == 0:
				logging.info ("{0} lines processed: {1}".format (srcfile, i+1))

	with open (os.path.join (dirname, tgtfile), "w") as fout:
		for word in sorted (V):
			fout.write ("{0},{1},{2},{3},{4}\n".format (word, Vlower[word], VUPPER[word], VTitle[word], V[word]))

if __name__ == "__main__":
	plac.call (main)
