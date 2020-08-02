import numpy as np
import scipy
import os
import logging
import plac
import sys
import ujson

from time import time
from collections import defaultdict, Counter

if "../" not in sys.path: sys.path.append ("../")

from modules.semshift import embeddings, alignment, docscores

logging.basicConfig (format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

UNK="UNK"

def readFeats (filename):
	feats = list ()
	with open (filename) as fin:
		for line in fin:
			feats.append (line.strip())
	return feats

def scoreMostProgressive (scorers, tokens, w2i, k=10):
	tokenset = set (tokens)
	scores_for_doc = [(UNK, -np.inf) if word not in tokenset else (word, scorers[word].score (tokens, w2i, window_size=k)) for word in scorers]	
	word, score = max (scores_for_doc, key=lambda x:x[1])
	return word, score

def scoreProgressive (scorers, tokens, w2i, k=10):
	tokenset = set (tokens)
	scores_for_doc = [{"word": word, "score": scorers[word].score (tokens, w2i, window_size=k)} for word in scorers if word in tokenset]
	return scores_for_doc

def scoreDocs (filename, early_model, later_model, words, check_nlines=10, stop_after=100, k=10):
	scores = list ()
	w2i, _ = early_model.index
	scorers = {word: docscores.Scorer (early_model, later_model, word) for word in words}
	with open (filename) as fin:
		for i, line in enumerate (fin):
			tokens = [token for token in line.strip().split(" ") if token.isalpha()]
			scores.append (scoreMostProgressive(scorers, tokens, w2i, k=k))
			#scores.append ({word: scorers[word].score (tokens, w2i, window_size=k) for word in words})
			#scores.append (scorer.score (tokens, w2i, window_size=k))
			if (i+1) % check_nlines == 0:
				logging.info ("Documents processed: {0}".format (i+1))
			if (i+1) == stop_after:
				break
	return scores

def scoreDocsAndWriteToFile (filename, early_model, later_model, words, output_file, check_nlines=10, stop_after=100, k=10):
	w2i, _ = early_model.index
	scorers = {word: docscores.Scorer (early_model, later_model, word) for word in words}
	with open (filename) as fin, open (output_file, "w") as fout:
		for i, line in enumerate (fin):	
			tokens = [token for token in line.strip().split(" ") if token.isalpha()]
			scores = scoreProgressive (scorers, tokens, w2i, k=k)
			fout.write (ujson.dumps (scores) + "\n")
			if (i+1) % check_nlines == 0:
				logging.info ("Documents processed: {0}".format (i+1))
			if (i+1) == stop_after:
				break
	
def read_vocab (filename):
	vocab = dict ()
	with open (filename) as fin:
		for line in fin:
			parts = line.strip().split("\t")
			w = parts[0]
			i = int(parts[1])
			vocab[w] = i

	return vocab

def make_common_vocab (V1, V2):
	# construct a common vocabulary
	W1 = {key for key in V1}
	W2 = {key for key in V2}

	C = W1 & W2
	return C

def intersection_align (M1, M2, V1, V2, C):
	""" M1 and V1 corresponds to the early model
		M2 and V2 corresponds to the later model
		C corresponds to the common vocabulary
	"""

	# index the early model based on the common vocabulary
	X1 = M1[[V1[w] for w in C],:]

	# index the later model based on the common vocabulary
	X2 = M2[[V2[w] for w in C], :]

	return X1, X2

def alignTwoModels (eC, eW, lC, lW, V1, V2):
	C = make_common_vocab (V1, V2)
	eC_, lC_ = intersection_align (eC, lC, V1, V2, C)
	eW_, lW_ = intersection_align (eW, lW, V1, V2, C)
	return eC_, eW_, lC_, lW_, C

def make_dict (vocab):
	w2i = {w: i for i, w in enumerate (vocab)}
	i2w = {i: w for i, w in enumerate (vocab)}
	return w2i, i2w

@plac.annotations (
	evf=("file with the early vocabulary", "positional"),
	lvf=("file with the later vocabulary", "positional"),
	ecf=("file with the early context vectors", "positional"),
	lcf=("file with the later context vectors", "positional"),
	ewf=("file with the early word(target) vectors", "positional"),
	lwf=("file with the later word(target) vectors", "positional"),
	shiftwordsfile=("file with the shifted words", "positional"),
	documentfile=("file containing the documents", "positional"),
	scoresfile=("file containing the document progressiveness score", "positional")
)
def main (evf, lvf, ecf, lcf, ewf, lwf, shiftwordsfile, documentfile, scoresfile):
	#shifted_words = readShiftedWords (shiftwordsfile)
	shifted_words = readFeats (shiftwordsfile)
	logging.info ("{0} file read; shifted words: {1}".format (shiftwordsfile, len(shifted_words)))

	# read the vocab
	early_vocab = read_vocab (evf)
	later_vocab = read_vocab (lvf)
	logging.info ("Read vocabulary from file ... done")

	# load the embedding matrices
	eC = np.load (ecf)
	eW = np.load (ewf)

	lC = np.load (lcf)
	lW = np.load (lwf)

	logging.info ("Load embeddings from file ... done")

	# align the two matrices
	eC_, eW_, lC_, lW_, common_vocab = alignTwoModels (eC, eW, lC, lW, early_vocab, later_vocab)

	w2i, i2w = make_dict (common_vocab)
	logging.info ("intersection alignment of both the models ... done")

	early = docscores.EmdsModel(eC_, eW_, (w2i, i2w))
	later = docscores.EmdsModel(lC_, lW_, (w2i, i2w))
		
	scoreDocsAndWriteToFile (documentfile, early, later, shifted_words, scoresfile, check_nlines=100000, stop_after=-1, k=10)	
	#scores = scoreDocs (documentfile, early, later, ["cloud"], check_nlines=100000, stop_after=-1, k=10)	
	logging.info ("computed scores for all the documents")

	#words = [w for w,s in scores]
	#progressiveness = np.array([s for w,s in scores])

	#with open (scoresfile, "w") as fout:
		#for i in range (len (scores)):
			#fout.write ("{0},{1}\n".format (words[i], progressiveness[i]))

if __name__ == "__main__":
	plac.call (main)
