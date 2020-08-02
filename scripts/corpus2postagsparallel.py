""" Run part of speech tagger on a document collection and for every distinct word,
	output the distribution of the part of speech tags """
import spacy
import ujson
import plac
import logging
import numpy as np

MAX_LENGTH = 1000000
nlp = spacy.load('en_core_web_sm')
nlp.max_length = MAX_LENGTH * 2
logging.basicConfig (format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

@plac.annotations(
	src=("the source filename", "positional"),
	rate=("the sampling rate", "option", None, float)
)
def main (src, rate=1.0):
	tgt = src.replace ("split", "pos")
	V = dict ()
	logging.info ("{0} Begin processing".format (src))
	nAccepted = 0
	
	with open (src) as fin:
		for i, line in enumerate (fin):
			if np.random.random () < rate:
				js = ujson.loads (line)
				text = " ".join (js["tokens"])
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
			if (i+1) % 10000 == 0:
				logging.info ("{0} lines read".format (i+1))

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
