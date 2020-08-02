""" Tokenize and tag documents from a .jsonl file """

import spacy
import ujson
import plac
import os
import sys
import logging

if "../../" not in sys.path:
	sys.path.append ("../../")

from modules import constants

TAGGED_EXT=".tokenized"

MAX_LENGTH = 10000000
NLP = spacy.load ("en_core_web_sm")
NLP.max_length = MAX_LENGTH

logging.basicConfig (format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

def tokenizeText (jurname, filesdir):
	with open (os.path.join (filesdir, jurname + constants.JSONL_EXT)) as fin, open (os.path.join (filesdir, jurname + TAGGED_EXT + constants.JSONL_EXT), "w") as fout:
		for i, line in enumerate (fin):
			js = ujson.loads (line)
			doc = NLP (js["text"], disable=["tagger", "parser", "ner"])
			tokens = [token.text.lower()  for token in doc]
			js["tokens"] = tokens
			fout.write (ujson.dumps (js) + constants.NL)

			if (i+1) % 1000 == 0:
				logging.info ("{0} lines processed for {1}".format (i+1, jurname))
				
@plac.annotations (
	filesdir = ("directory with input files and output files", "positional"),
	jurname=("the jurisdiction name", "positional")
)
def main (filesdir, jurname):
	tokenizeText (jurname, filesdir)

if __name__ == "__main__":
	plac.call (main)
