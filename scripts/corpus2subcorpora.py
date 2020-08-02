import plac
import ujson
import logging
import datetime
import os
import math

logging.basicConfig (format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

def dividebytime(src, tgt, since, until, period):
	""" divide the text corpus into multiple smaller corpora,
		each spanning a given number of years

		parameters
		----------
		src: str
			input file
		
		tgt: str
			output dir

		since: int
			starting from (and including) this year

		until: int
			before this year
		
		period: int
			number of years for each (sub)corpus.
	"""
	N = math.ceil((until - since) / period)
	file_prefixes = range (N)
	
	filehandles = {file_prefix:open(os.path.join (tgt, "{0}.jsonl".format (file_prefix)), "w") for file_prefix in file_prefixes}

	# go over the entire corpus and divide them into subcorpus
	with open (src) as fin:
		for i, line in enumerate(fin):
			js = ujson.loads (line.strip())
			year = js["year"]
			bucket = int ((year - since) / period)
			if year >= since and year <= until and bucket in filehandles:
				filehandles[bucket].write (ujson.dumps (js) + "\n")


	# close all the filehandles
	for key in filehandles:
		filehandles[key].close()
	
	# for convenience, write the mapping between filenames and the years in which they belong
	with open (os.path.join (tgt, "filename_periods.csv"), "w") as fout:
		for key in sorted (filehandles.keys()):
			s = since + (key * period)
			fout.write ("{0},{1},{2}\n".format (key, s, s+period-1))

def dividebydocs(src, tgt, n):
	""" divide the text corpus into multiple smaller corpora,
		each spanning approximately the same number of documents

		parameters
		----------
		src: str
			input file
		
		tgt: str
			output dir

		n: int
			the number of splits

	"""
	with open (src) as fin:
		for docs,_ in enumerate (fin):
			pass

	docs = docs + 1

	docs_per_split = int(docs / n)

	split = 0
	file_prefixes = dict ()
	with open (src) as fin:
		fout = open (os.path.join (tgt, "{0}.jsonl".format (split)), "w")
		for i, line in enumerate (fin):
			if ((i+1) % docs_per_split) == 0 and split < n:
				fout.write (line)
				fout.close()
				file_prefixes[split] = i+1
				split += 1
				fout = open (os.path.join (tgt, "{0}.jsonl".format (split)), "w")
			fout.write (line)
		fout.close()
		file_prefixes[split] = i

	with open (os.path.join (tgt, "filename_docs.csv"), "w") as fout:
		for key in sorted (file_prefixes.keys()):
			fout.write ("{0},{1}\n".format (key, file_prefixes[key]))

@plac.annotations(	
	split=("The type of split", "positional", None, str, ["time", "docs"]),
	src=("the input file with the entire corpus", "positional"),
	tgt=("place the output files in this directory", "positional", None, str),
	since=("in or after this year (only used if split is time)", "option", "s", int),
	until=("before this year (only used if split is time)", "option", "u", int),
	period=("the interval (only used if split is time)", "option", "p", int),
	n=("the number of splits (only used if the split is docs)", "option", "n", int)
)
def main (split, src, tgt, since=1950, until=1955, period=5, n=8):
	os.makedirs (tgt, exist_ok=True) #create the directory if it doesn't exist.
	if split == "time":
		dividebytime (src, tgt, since, until, period)
	elif split == "docs":
		dividebydocs (src, tgt, n)
	else:
		print ("Unknown option")

if __name__ == "__main__":
	plac.call (main)
