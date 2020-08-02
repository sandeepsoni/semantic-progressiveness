import plac
import numpy as np
import pandas as pd

@plac.annotations (
	changewordsfile=("words and their scores according to semantic change metric", "positional"),
	nounprobfile=("the probability of the word being a proper noun", "positional"),
	prunedwordsfile=("words that are stronger candidates for being semantic changes", "positional"),
	percentile=("remove words whose noun probability is above this percentile", "option", None, int),
	topk=("write the topk words that have changed the most to file", "option", None, int)
)
def main (changewordsfile, nounprobfile, prunedwordsfile, percentile=75, topk=1000):
	changewords = pd.read_csv (changewordsfile, sep=",", header=None, names=["word", "score"])
	nounprob = pd.read_csv (nounprobfile, sep="\t", header=None, names=["word", "prob"])
	names = nounprob[nounprob.prob >= np.percentile(nounprob.prob,percentile)]
	pruned = set (list (changewords.word.values[:topk]))- set (list (names.word.values))

	with open (prunedwordsfile, "w") as fout:
		for word in changewords.word.values[:topk]:
			if word in pruned:
				fout.write ("{0}\n".format (word))

if __name__ == "__main__":
	plac.call (main)
