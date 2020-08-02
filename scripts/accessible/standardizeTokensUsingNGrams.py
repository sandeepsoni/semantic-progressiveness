"""
To standardize the tokens based on google n-gram frequencies. 
The case study is to segment words that are glued together. 
The basic idea can be explained with an example. 

Suppose there is a token "senatoradmits", we want to segment it as "senator" and "admits" if 
`count("senator") + count("admits") > count ("senatoradmits")`. 

Furthermore, if we have some context like "x senatoradmits y", then we want to segment to "senator" and admits if 
`count ("x senator") + count ("senator admits") + count("admits y") > count("x senatoradmits") + count ("senatoradmits y") `.

All the counts are calculated using goolge n-grams and are restricted according to years.
"""


import plac
import ujson
from collections import defaultdict
import pandas as pd
import logging
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class TokensFileReader (object):
	def __init__ (self, filename):
		self.filename = filename

	def read (self, nlines=10):
		with open (self.filename) as fin:
			for i, line in enumerate (fin):
				js = ujson.loads (line)
				yield js
	
def writeSubs (subs, subsfile):
	with open (subsfile, "w") as fout:
		for w in subs:
			fout.write ("==>".join ([w, subs[w]]) + "\n")

def writeStandardFile (tokensfile, subs, standardizedfile):
	with open (tokensfile) as fin, open (standardizedfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			standard_tokens = list ()
			for token in js["tokens"]:
				if token in subs:
					standard_tokens.extend (subs[token].split(" "))
				else:
					standard_tokens.append (token)

			js["clean_tokens"] = standard_tokens
			fout.write(ujson.dumps (js) + "\n")


def segment (word):
	cands = set ()
	for i,char in enumerate (word):
		part1, part2 = word[:i], word[i:]
		if part1 != "" and part2 != "":
			cands.add ((part1, part2))

	return cands

def getSubsByUnigramBigramComparison (grams1, grams2, tokensfile):
	"""
	TODO: consider using lower case counts if sparsity is causing weird segmentations
	"""
	subs = dict ()
	reader = TokensFileReader (tokensfile)
	for js in reader.read():
		tokens = js["tokens"]
		for token in tokens:
			if token in subs:
				continue
			count_token = grams1[(token,)]
			cands = segment (token)	
				
			standardized = token
			count_segments = [(cand1, cand2, grams2[(cand1, cand2)]) for cand1, cand2 in cands if grams2[(cand1, cand2)] > count_token]
			if len (count_segments) > 0:
				best_cand1, best_cand2, _ = max (count_segments, key=lambda x:x[2])
				standardized = " ".join ([best_cand1, best_cand2])

			subs[token] = standardized

	return subs	

def find_ngrams(input_list, n):
	return zip(*[input_list[i:] for i in range(n)])	

def getSubsByBigramTrigramComparison (grams2, grams3, tokensfile, subsfile, standardizedfile):
	reader = TokensFileReader (tokensfile)
	with open (standardizedfile, "w") as fout, open (subsfile, "w") as subsout:
		for js in reader.read():
			tokens = js["tokens"]
			clean_tokens = list ()
			if len (tokens) > 0: clean_tokens.append (tokens[0]) # add the first token
			for lc, token, rc in find_ngrams (tokens, 3):
				standardized = token
				if token.isalpha(): # don't try if not alphabetic
					lhs = grams2[(lc, token)] + grams2[(token, rc)]
					cands = segment (token)
	
					count_segments = [(cand1, cand2, grams3[(lc, cand1,cand2)] + grams3[(cand1,cand2,rc)]) 
									  for cand1,cand2 in cands
									  if grams3[(lc, cand1, cand2)] + grams3[(cand1, cand2, rc)] > lhs]

					if len (count_segments) > 0:
						best_cand1, best_cand2, best_val = max (count_segments, key=lambda x:x[2])
						standardized = " ".join ([best_cand1, best_cand2])

					subsout.write ("{} ==> {}\n".format (token, standardized))

				clean_tokens.append (standardized)
			if len (rc) > 0: clean_tokens.append (rc) # add the last token
		
			js["clean_tokens"] = clean_tokens
			fout.write (ujson.dumps (js) + "\n")

def readNgramsAsDict (filename):
	grams = defaultdict (int)
	with open (filename) as fin:
		for line in fin:
			parts = line.strip().split ("\t")
			grams[tuple(parts[0].split())] = int(parts[1])
	return grams

@plac.annotations (
	tokensfile = ("the tokens file", "positional"),
	unigramsfile=("the file containing the unigram counts", "positional"),
	bigramsfile=("the file containing the bigram counts", "positional"),
	trigramsfile=("the file containing the trigram counts", "positional"),
	subsfile=("the file containing the substitutions"),
	standardizedfile = ("the normalized file", "positional")
)
def main (tokensfile, unigramsfile, bigramsfile, trigramsfile, subsfile, standardizedfile):
	#grams1 = readNgramsAsDict (unigramsfile)
	#logging.info ("Unigrams reading ... complete")
	grams2 = readNgramsAsDict (bigramsfile)
	logging.info ("Bigrams reading ... complete")
	grams3 = readNgramsAsDict (trigramsfile)
	logging.info ("Trigrams reading ... complete")

	# Substitutions file using unigram, bigram comparison, using bigram-trigram comparison.

	#subs1 = getSubsByUnigramBigramComparison(grams1, grams2, tokensfile)
	getSubsByBigramTrigramComparison(grams2, grams3, tokensfile, subsfile, standardizedfile)

if __name__ == "__main__":
	plac.call (main)
