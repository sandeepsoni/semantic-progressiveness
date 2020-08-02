import numpy as np
import plac
import os

@plac.annotations(
	idsfile=("file with the ids", "positional"),
	linenumsfile=("file containing linenums", "positional"),
	nlines=("the size of the sample", "option", None, int)
)
def main (idsfile, linenumsfile, nlines=100000):
	np.random.seed (314)
	with open (idsfile) as fin:
		ids = [line.strip() for line in fin]

	nids = len (ids)
	linenums = np.random.choice (nids, nlines, replace=False)

	with open (linenumsfile, "w") as fout:
		for linenum in linenums:
			fout.write ("{0}\n".format (linenum))

if __name__ == "__main__":
	plac.call(main)
