import os
import sys
import numpy as np
import plac

if "../../" not in sys.path: sys.path.append ("../../")

from modules.semshift import embeddings, alignment, measures

STATS_DIR = "/hg191/corpora/legaldata/data/stats"
MODELS_DIR = "/hg191/corpora/legaldata/models"

NAMES_FILES = [os.path.join (STATS_DIR, "names.neural"), os.path.join (STATS_DIR, "names.tagging")]

def readNames (filenames):
	names = set ()
	for filename in filenames:
		with open (filename) as fin:
			for line in fin:
				names.add (line.strip())

	return names

def alignTwoModels (first_model, second_model):
	second_model.m = alignment.smart_procrustes_align_gensim (first_model.m, second_model.m)
	return first_model, second_model

@plac.annotations(
	seed=("seed value", "positional", None, int)
)
def main (seed):
	names = readNames (NAMES_FILES)
	earlym = embeddings.TrainedModel(os.path.join(MODELS_DIR, "sgns.500K.early.{0}.model".format (seed)))
	laterm = embeddings.TrainedModel(os.path.join(MODELS_DIR, "sgns.500K.later.{0}.model".format (seed)))

	print ("Loaded the two models from file")
	earlym_, laterm_ = alignTwoModels (earlym, laterm)

	print ("Aligned the two models")

	vEarly = {key for key in earlym_.m.wv.vocab.keys()}
	vLater = {key for key in earlym_.m.wv.vocab.keys()}

	vCommon = vEarly & vLater

	V = vCommon - names
	print ("Built comon vocabulary without names")

	scores = dict ()
	for i,w in enumerate (V):
		scores[w] = measures.HamiltonMeasures.cultural_shift (earlym_.m, laterm_.m, w, k=50)

		if (i+1) % 1000 == 0:
			print ("Words processed: {0}".format (i+1))

	targetfile = os.path.join (STATS_DIR, "V.{0}.scores".format (seed))	
	with open (targetfile, "w") as fout:
		for w, score in sorted (scores.items(), key=lambda x:x[1], reverse=True):
			fout.write ("{0},{1}\n".format (w, score))

if __name__ == "__main__":
	plac.call(main)
