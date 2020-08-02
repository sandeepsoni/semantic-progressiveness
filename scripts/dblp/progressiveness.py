import numpy as np
import scipy
import os
import logging
import plac
import sys
import ujson

from time import time
from collections import defaultdict, Counter

if "../../" not in sys.path: sys.path.append ("../../")

from modules.semshift import embeddings, alignment, docscores

logging.basicConfig (format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)

UNK="UNK"

def readFeats (filename):
	feats = list ()
	with open (filename) as fin:
		for line in fin:
			feats.append (line.strip())
	return feats

def alignTwoModels (first_model, second_model):
	second_model.m = alignment.smart_procrustes_align_gensim (first_model.m, second_model.m)
	return first_model, second_model

def alignTwoModels2 (first_model, second_model):
	# just intersect the vocabulary and align the word indices
	first_model.m, second_model.m = alignment.intersection_align_gensim (first_model.m, second_model.m)
	return first_model, second_model

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
			

@plac.annotations (
	earlymodelfile=("file with the early model", "positional"),
	latermodelfile=("file with the later model", "positional"),
	shiftwordsfile=("file with the shifted words", "positional"),
	documentfile=("file containing the documents", "positional"),
	scoresfile=("file containing the document progressiveness score", "positional")
)
def main (earlymodelfile, latermodelfile, shiftwordsfile, documentfile, scoresfile):
	#shifted_words = readShiftedWords (shiftwordsfile)
	shifted_words = readFeats (shiftwordsfile)
	logging.info ("{0} file read; shifted words: {1}".format (shiftwordsfile, len(shifted_words)))

	early_origmodel = embeddings.TrainedModel (earlymodelfile)
	later_origmodel = embeddings.TrainedModel (latermodelfile)

	# alignment using procrustes method
	earlymodel, latermodel = alignTwoModels2 (early_origmodel, later_origmodel)

	logging.info ("alignment of both the models done")

	i2w = {i:w for i, w in enumerate (earlymodel.m.wv.index2word)}
	w2i = {w:i for i, w in enumerate (earlymodel.m.wv.index2word)}
	early = docscores.EmdsModel(earlymodel.m.trainables.syn1neg, earlymodel.m.wv.vectors, (w2i, i2w))
	later = docscores.EmdsModel(latermodel.m.trainables.syn1neg, latermodel.m.wv.vectors, (w2i, i2w))
		
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
