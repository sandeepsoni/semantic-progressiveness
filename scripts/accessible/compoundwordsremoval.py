import plac
import logging

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def list2index (items):
	idx = {item: i for i, item in enumerate (items)}
	iidx = {i:item for i, item in enumerate (items)}
	return idx, iidx

def getNGramCounts (corpusfile, n=2):
	vectorizer = CountVectorizer (decode_error="ignore", ngram_range=(n,n))
	X = vectorizer.fit_transform (open (corpusfile))
	features = vectorizer.get_feature_names ()
	return X, list2index (features)
	
def segment (word):
	cands = set ()
	for i,char in enumerate (word):
		part1, part2 = word[:i], word[i:]
		if part1 != "" and part2 != "":
			cands.add ((part1, part2))

	return cands

def NBSegmentation (DT, index, changewords):
	z = np.log(DT.sum())
	C = np.log(DT.sum(axis=0)) # sum all the rows
	idx, iidx = index
	okaywords = list ()

	
	for word in changewords:
		if word not in idx:
			okaywords.append (word) #nothing can be done about this word
		else:
			cands = segment (word)
			hasValidSegment=False
			for w1, w2 in cands:
				isPresent = w1 in idx and w2 in idx
				if isPresent and ((z+C[0, idx[word]]) < (C[0, idx[w1]] + C[0, idx[w2]])):
					hasValidSegment=True
					break

			if not hasValidSegment:
				okaywords.append (word)

	return okaywords

@plac.annotations (
	changefile=("file containing words that changed", "positional"),
	corpusfile=("file containing documents per line", "positional"),
	prunedfile=("file containing change words but without the compund words", "positional"),
	topk=("take only the first k words", "option", None, int)
)
def main (changefile, corpusfile, prunedfile, topk=2500):
	changewords = pd.read_csv (changefile, sep=",", header=None, names=["word"])
	logging.info ("Changewords read")
	X, index = getNGramCounts (corpusfile, n=1)
	logging.info ("Document-Term matrix created")
	okaywords = NBSegmentation (X, index, changewords.word.values)	
	logging.info ("Changewords pruned")
	with open (prunedfile, "w") as fout:
		for word in okaywords[:topk]:
			fout.write ("{0}\n".format (word))
	logging.info ("Changewords written to file")

if __name__ == "__main__":
	plac.call (main)
