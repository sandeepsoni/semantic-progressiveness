""" Converts each document in the corpus as as list of tokens."""

import plac
import ujson
import numpy as np
import spacy

NLP = spacy.load('en_core_web_sm')

def tokenize (text):
	doc = NLP (text, disable=["parser", "tagger", "ner"])
	tokens = [token.text for token in doc]
	return tokens
	
@plac.annotations(
	src=("source file with one document as a json per line", "positional"),
	tgt=("target file with one document as a json per line", "positional"),
	lines=("read lines at a time", "option", None, int)
)
def main (src, tgt, lines=10000):
	with open (src) as fin, open (tgt, "w") as fout:
		records = list ()
		for i, line in enumerate (fin):
			js = ujson.loads (line)
			records.append (js)
			if (i+1) % lines == 0:
				for record in records:
					tokens = tokenize (record["text"])
					record["tokens"] = tokens
					fout.write (ujson.dumps (record) + "\n")

				fout.flush()
				records = list ()

		if len (records) > 0:
			for record in records:
				tokens = tokenize (record["text"])
				record["tokens"] = tokens
				fout.write (ujson.dumps (record) + "\n")

if __name__ == "__main__":
	plac.call(main)
