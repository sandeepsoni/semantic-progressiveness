""" Converts each document in the corpus as as list of tokens.

Time taken for the legal opinions corpus:
real    1826m25.716s
user    1809m46.362s
sys     14m13.467s


Time taken for the academic articles corpus:
"""

import plac
import ujson
import numpy as np
from bs4 import BeautifulSoup
import spacy
import datetime

NLP = spacy.load('en_core_web_sm')

def tokenize (text):
	doc = NLP (text, disable=["parser", "tagger", "ner"])
	tokens = [token.text for token in doc]
	return tokens

def readAndWrite (key, src, tgt, since, until, linesInChunk=1000):
	with open (src) as fin, open (tgt, "w") as fout:
		records = list ()
		for i, line in enumerate (fin):
			js = ujson.loads (line)
			records.append (js)
			if (i+1) % linesInChunk == 0:
				for record in records:
					if record["year"] >= since and record["year"] <= until:
						record["tokens"] = tokenize(record[key])
						fout.write (ujson.dumps (record) + "\n")
				fout.flush ()
				records = list ()

		if len (records) > 0:
			for record in records:
				if record["year"] >= since and record["year"] <= until:
					record["tokens"] = tokenize (record[key])
					fout.write (ujson.dumps (record) + "\n")	
				
@plac.annotations(
	key=("key in json whose value should be tokenized", "positional", None, str, ["text", "abstract"]),
	src=("source file with one document as a json per line", "positional"),
	tgt=("target file with one document as a json per line", "positional"),
	since=("from year", "option", None, int),
	until=("upto year", "option", None, int)
)
def main (key, src, tgt, since=1951, until=2010):
	readAndWrite (key, src, tgt, since, until, linesInChunk=1000)

if __name__ == "__main__":
	plac.call(main)
