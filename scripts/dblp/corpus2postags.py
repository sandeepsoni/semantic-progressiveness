""" Run part of speech tagger on a document collection and for every distinct word,
	output the distribution of the part of speech tags """
import spacy
import plac
import logging
import numpy as np
import os

MAX_LENGTH = 100000
nlp = spacy.load('en_core_web_sm')
nlp.max_length = MAX_LENGTH
logging.basicConfig (format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

@plac.annotations(
	srcdir=("the source directory", "positional"),
	srcfile=("the source file", "positional"),
	rate=("the sampling rate", "option", None, float)
)
def main (srcdir, srcfile, rate=1.0):
	src = os.path.join (srcdir, srcfile)
	tgt = os.path.join (srcdir, os.path.splitext (srcfile)[0] + ".pos")
	V = dict ()
	logging.info ("{0} Begin processing".format (src))

	nAccepted = 0
	nlines = 0
	with open (src) as fin:
		for line in fin:
			nlines += 1

	logging.info ("{0} contains {1} lines".format (src, nlines))

	linenums = set (list (np.random.choice (nlines, int(rate * nlines), replace=False)))
	logging.info ("No. of samples to be used: {0}(sampling rate: {1})".format (len(linenums), rate))
	
	with open (src) as fin:
		for i, line in enumerate (fin):
			if i in linenums:
				text = line.strip()
				doc = nlp (text, disable=["parser", "ner"])
				for token in doc:
					t = token.text.lower()
					tag = token.tag_
					if t not in V:
						V[t] = dict ()
					if tag not in V[t]:
						V[t][tag] = 0
					V[t][tag] += 1
				nAccepted += 1
			if (i+1) % 1000 == 0:
				logging.info ("{0} lines read; {1} accepted so far".format (i+1, nAccepted))

	logging.info ("{0} Total lines accepted: {1}/{2}".format (src, nAccepted, i+1))

	with open (tgt, "w") as fout:
		for w in V:
			fout.write ("{0}".format (w))
			for tag in V[w]:
				fout.write ("\t")
				fout.write ("{0}:{1}".format (tag, V[w][tag]))
			fout.write ("\n")
	

if __name__ == "__main__":
	plac.call (main)
