""" Make a easy to use processed corpus file.
"""

import ujson
import plac
import glob
import numpy as np
import tempfile
import heapq
import os
import shutil
import datetime
from bs4 import BeautifulSoup

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
		keys = ["id", "name", "court", "date", "text"]
		return np.all ([key in record for key in keys]) and len (record["text"]) > 0

	outjs = {}
	isok=False
	if meetscondition (injs):
		outjs["id"] = injs["id"]
		outjs["name"] = injs["name"]
		outjs["court"] = injs["court"]
		outjs["date"] = injs["date"]
		outjs["year"] = datetime.datetime.fromtimestamp(injs["date"]).year
		soup = BeautifulSoup (injs["text"], "html5lib")
		outjs["text"] = soup.get_text().replace ("\n", " ")
		isok = True
	return outjs, isok

def filterAndAggregate (src, tgt):	
	fout = open (tgt, "w")
	with open (src) as fin:
		for line in fin:
			js = ujson.loads (line.strip())
			js, isok = mapjson (js)
			if isok: fout.write (ujson.dumps(js) + "\n")

	fout.close()

@plac.annotations(
	src=("the source file", "positional"),
	tgt=("the target file with the entire corpus", "positional"),
	tmpdir=("the temporary directory", "positional")
)
def main (src, tgt, tmpdir):
	if not os.path.exists (tmpdir):
		os.makedirs (tmpdir)
	filterAndAggregate (src, tgt)
	chunkAndSort(tgt, tmpdir, n=1000000)
	mergeAndWrite (tgt, tmpdir)
	shutil.rmtree (tmpdir)

if __name__ == "__main__":
	plac.call (main)
