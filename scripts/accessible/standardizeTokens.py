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
				yield " ".join (js["tokens"])
				if (i+1) == nlines:
					break

def list2index (items):
	idx = {item: i for i, item in enumerate (items)}
	iidx = {i:item for i, item in enumerate (items)}
	return idx, iidx

def getNGramCounts (corpusfile, n=2):
	vectorizer = CountVectorizer (decode_error="ignore", ngram_range=(n,n))
	tfreader = TokensFileReader (corpusfile)
	X = vectorizer.fit_transform (tfreader.read(nlines=400000))
	features = vectorizer.get_feature_names ()
	return X, list2index (features)

def segment (word):
	cands = set ()
	for i,char in enumerate (word):
		part1, part2 = word[:i], word[i:]
		if part1 != "" and part2 != "":
			cands.add ((part1, part2))

	return cands

def NBSegmentation (vocab, DT, index):
	z = np.log(DT.sum())
	C = np.log(DT.sum(axis=0)) # sum all the rows
	idx, iidx = index
	
	subs = dict ()
	for w in vocab:
		if w not in idx:
			subs[w] = w
		else:
			pw = (z+C[0,idx[w]])
			cands = segment (w)
			pcands = [(w1, w2, C[0,idx[w1]] + C[0,idx[w2]]) for w1, w2 in cands if w1 in idx and w2 in idx]
			if len (pcands) > 0:
				bestw1, bestw2, score = max (pcands, key=lambda x:x[2])
				if pw < score:
					subs[w] = " ".join ([bestw1, bestw2])
				else:
					subs[w] = w
			else:
				subs[w] = w

	return subs

def readVocab (vocabfile):
	V = set ()
	with open (vocabfile) as fin:
		for line in fin:
			parts = line.strip().split ("\t")
			if parts[0].isalpha():
				V.add (parts[0])
	return V

def getSubs (vocabfile, tokensfile):
	V = readVocab (vocabfile)
	X, index = getNGramCounts (tokensfile, n=1)
	logging.info ("Document-Term matrix")

	subs = NBSegmentation (V, X, index)
	return subs	
	
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

@plac.annotations (
	tokensfile = ("the tokens file", "positional"),
	vocabfile = ("the file containing the vocab", "positional"),
	subsfile=("the file containing the substitutions"),
	standardizedfile = ("the normalized file", "positional")
)
def main (tokensfile, vocabfile, subsfile, standardizedfile):
	subs = getSubs(vocabfile, tokensfile)
	writeSubs (subs, subsfile)
	writeStandardFile (tokensfile, subs, standardizedfile)

if __name__ == "__main__":
	plac.call (main)
