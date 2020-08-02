""" extract the text field and create a text file (ignore all the other fields)

Notes
=====

- takes around 15 minutes on a corpus of ~300k documents
"""
import ujson
import plac
import numpy as np


@plac.annotations (
	src=("source file", "positional"),
	tgt=("target file", "positional"),
)
def main (src, tgt):
	with open (src) as fin:
		for i, line in enumerate (fin):
			pass

	with open (src) as fin, open (tgt, "w") as fout:
		for i, line in enumerate (fin):
			js = ujson.loads (line.strip())
			text = " ".join ([token.lower () for token in js["tokens"] if token.isalpha()])
			fout.write (text)
			fout.write ("\n")

if __name__ == "__main__":
	plac.call (main)
