import os
import sys
import numpy as np
import plac

if "../../" not in sys.path: sys.path.append ("../../")

from modules.semshift import embeddings, alignment, measures

def alignTwoModels (first_model, second_model):
	second_model.m = alignment.smart_procrustes_align_gensim (first_model.m, second_model.m)
	return first_model, second_model

@plac.annotations(
	earlymodelfile=("file containing the early model", "positional"),
	latermodelfile=("file containing the later model", "positional"),
	tgtfile=("file to output with the change list and their scores", "positional")
)
def main (earlymodelfile, latermodelfile, tgtfile):
	earlymodel = embeddings.TrainedModel(earlymodelfile)
	latermodel = embeddings.TrainedModel(latermodelfile)

	earlymodel_, latermodel_ = alignTwoModels (earlymodel, latermodel)

	early_vocab = {key for key in earlymodel_.m.wv.vocab.keys()}
	later_vocab = {key for key in latermodel_.m.wv.vocab.keys()}

	common_vocab = early_vocab & later_vocab

	scores = dict ()
	for i,w in enumerate (common_vocab):
		scores[w] = measures.HamiltonMeasures.cultural_shift (earlymodel_.m, latermodel_.m, w, k=50)

		if (i+1) % 1000 == 0:
			print ("Words processed: {0}".format (i+1))	

	with open (tgtfile, "w") as fout:
		for w, score in sorted (scores.items(), key=lambda x:x[1], reverse=True):
			fout.write ("{0},{1}\n".format (w, score))

if __name__ == "__main__":
	plac.call(main)
