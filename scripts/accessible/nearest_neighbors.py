import plac
import sys

if "../../" not in sys.path: sys.path.append ("../../")

from modules.semshift import embeddings, alignment

def readVocab (filename):
	vocab = list ()
	with open (filename) as fin:
		for line in fin:
			vocab.append (line.strip())

	return vocab

def alignTwoModels (first_model, second_model):
	second_model.m = alignment.smart_procrustes_align_gensim (first_model.m, second_model.m)
	return first_model, second_model

@plac.annotations(
	earlymodelfile=("file containing the early model", "positional"),
	latermodelfile=("file containing the later model", "positional"),
	srcfile=("file containing the words", "positional"),
	tgtfile=("file containing the nearest neighbors for every word in the list", "positional")
)
def main (earlymodelfile, latermodelfile, srcfile, tgtfile):
	earlymodel = embeddings.TrainedModel (earlymodelfile)
	latermodel = embeddings.TrainedModel (latermodelfile)

	earlymodel_, latermodel_ = alignTwoModels (earlymodel, latermodel)
	vocab = readVocab (srcfile)

	with open (tgtfile, "w") as fout:
		for w in vocab:
			most_similar_before = list (map (lambda x:x[0], earlymodel_.m.most_similar (positive=w, topn=10)))
			most_similar_after = list (map (lambda x:x[0], latermodel_.m.most_similar (positive=w, topn=10)))

			fout.write ("{0}\n".format (w))
			fout.write ("before: " + ",".join (most_similar_before) + "\n")
			fout.write ("after: " + ",".join (most_similar_after) + "\n")
			
			fout.write ("\n")

if __name__ == "__main__":
	plac.call (main)
