""" Filter out certain keys and put all examples from different files into one file.

Time taken by the script:

real    46m36.857s
user    39m35.356s
sys     3m38.294s
"""

import ujson
import plac
import glob
import numpy as np
import tempfile
import heapq
import os
import shutil

def chunkAndSort (filename, tmpdir, n=10000):
	lines = list ()
	with open (filename) as fin:
		for i, line in enumerate (fin):
			lines.append (line)
			if (i+1) % n == 0:
				with tempfile.NamedTemporaryFile (mode="w+t", suffix=".jsl", dir=tmpdir, delete=False) as fout:
					for line in sorted (lines, key=lambda x:ujson.loads (x)["year"]):
						fout.write (line)
				lines = list ()
		
		if len (lines) > 0:
			with tempfile.NamedTemporaryFile (mode="w+t", suffix=".jsl", dir=tmpdir, delete=False) as fout:
				for line in sorted (lines, key=lambda x:ujson.loads (x)["year"]):
					fout.write (line)
				lines = list ()

def line_iterator (filename):
	with open (filename) as fin:
		for line in fin:
			yield line.strip()

def mergeAndWrite (filename, tmpdir):
	iterables = [line_iterator (name) for name in glob.glob (os.path.join (tmpdir, "*.jsl"))]
	with open (filename, "w") as fout:
		merged = heapq.merge (*iterables, key=lambda x:ujson.loads(x)["year"])
		for line in merged:
			fout.write (line + "\n")

def mapjson (injs):
	def meetscondition (record):
		keys = ["year", "id", "venue", "title", "paperAbstract", "outCitations", "inCitations", "authors", "entities", "journalName", "journalPages"]
		return np.all ([key in record for key in keys]) and len (record["paperAbstract"]) > 0

	outjs = {}
	isok=False
	if meetscondition (injs):
		outjs["year"] = injs["year"]
		outjs["id"] = injs["id"]
		outjs["venue"] = injs["venue"]
		outjs["title"] = injs["title"]
		outjs["abstract"] = injs["paperAbstract"]
		outjs["outcites"] = injs["outCitations"]
		outjs["incites"] = injs["inCitations"]
		outjs["journame"] = injs["journalName"]
		outjs["entities"] = injs["entities"]
		outjs["pages"] = injs["journalPages"]
		outjs["nauthors"] = len(injs["authors"])
		isok = True
	return outjs, isok

def filterAndAggregate (pattern, tgt):	
	fout = open (tgt, "w")
	for filename in glob.glob (pattern):
		with open (filename) as fin:
			for line in fin:
				js,isok = mapjson (ujson.loads (line.strip()))
				if isok: fout.write (ujson.dumps(js) + "\n")

	fout.close()

@plac.annotations(
	pattern=("the pattern of all individual files", "positional"),
	tgt=("the target file with the entire corpus", "positional"),
	tmpdir=("the temporary directory", "positional")
)
def main (pattern, tgt, tmpdir):
	os.makedirs (tmpdir, exist_ok=True)
	filterAndAggregate (pattern, tgt)
	chunkAndSort(tgt, tmpdir, n=1000000)
	mergeAndWrite (tgt, tmpdir)
	shutil.rmtree (tmpdir)

if __name__ == "__main__":
	plac.call (main)
