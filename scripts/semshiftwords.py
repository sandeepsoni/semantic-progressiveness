import numpy as np
import argparse
from sklearn.preprocessing import normalize
import scipy
import logging

logging.basicConfig (format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO)

def getArgs ():
	parser = argparse.ArgumentParser ()
	parser.add_argument ("--early-model", type=str, required=True, help="embeddings of the early model")
	parser.add_argument ("--later-model", type=str, required=True, help="embeddings of the later model")
	parser.add_argument ("--early-vocab", type=str, required=True, help="the early vocabulary")
	parser.add_argument ("--later-vocab", type=str, required=True, help="the later vocabulary")
	parser.add_argument ("--features-file", type=str, required=True, help="the features file")
	parser.add_argument ("--common-vocab-file", type=str, required=True, help="the common vocabulary file")
	args = parser.parse_args ()
	return args

def read_vocab (filename):
	vocab = dict ()
	with open (filename) as fin:
		for line in fin:
			parts = line.strip().split("\t")
			w = parts[0]
			i = int(parts[1])
			vocab[w] = i

	return vocab

def intersection_align (M1, M2, V1, V2):
	""" M1 and V1 corresponds to the early model
		M2 and V2 corresponds to the later model
	"""

	# construct a common vocabulary
	W1 = {key for key in V1}
	W2 = {key for key in V2}

	C = W1 & W2

	# index the early model based on the common vocabulary
	X1 = M1[[V1[w] for w in C],:]

	# index the later model based on the common vocabulary
	X2 = M2[[V2[w] for w in C], :]

	return X1, X2, C

def procrustes (A, B):
	U, _, Vt = scipy.linalg.svd(B.dot(A.T))
	print (U)
	print (Vt)
	return U.dot(Vt)
	return 0

def alignTwoModels (M1, M2, V1, V2):
	X1, X2, C = intersection_align (M1, M2, V1, V2)
	#R = procrustes (X1, X2)
	#return np.dot (R,X1), X2, C
	return X1, X2, C

def most_similar (mat, vocab, word):
	w2i,i2w = vocab
	sim = np.dot (mat, mat[w2i[word], :].T)
	sim = np.squeeze (sim)
	indices = np.argsort (-sim)
	nns = [(i2w[ind], sim[ind]) for ind in indices if not i2w[ind]==word]
	return nns

def cultural_shift (M1, M2, V, word, k=10):
	""" Hamilton et al. (2016) also proposed a measure for cultural shift,
		which is a local measure in which every word is represented by two
		d-dimensional vectors. d is the size of the set obtained by taking
		a union of two sets: k nearest neighbors based on the `before` model
		and the k nearest neighbor in the `after` model. Thus, k<=d<=2k.
		Each component in the d-dimensional vector is the cosine similarity
		of the `word` with that other word.

		The measure is simply the cosine distance between the two d-dimensional
		vectors.

		Parameters
		----------

		:before,after: Embedding matrices
		:word: str
			word for which the measure is to be calculated

		:k: int, the number of nearest neighbors

	"""
	w2i,i2w = V
	nn1 = most_similar (M1, V, word)
	nn2 = most_similar (M2, V, word)

	NN1 = dict (nn1)
	NN2 = dict (nn2)

	common = set ([w for w,_ in nn1[:k]]) | set ([w for w,_ in nn2[:k]])
	sim1 = np.array ([NN1[w] for w in common])
	sim2 = np.array ([NN2[w] for w in common])

	sim = np.dot (sim1, sim2)/(np.linalg.norm (sim1) * np.linalg.norm (sim2))
	return 1-sim

def make_dict (vocab):
	w2i = {w: i for i, w in enumerate (vocab)}
	i2w = {i: w for i, w in enumerate (vocab)}
	return w2i, i2w

def write_vocab (vocab, filename):
	with open (filename, "w", encoding="utf-8") as fout:
		for w in vocab:
			fout.write ("{}\t{}\n".format (w, vocab[w]))

def main (args):
	# read the vocab
	early_vocab = read_vocab (args.early_vocab)
	later_vocab = read_vocab (args.later_vocab)
	logging.info ("Read vocabulary from file ... done")

	# load the embedding matrices
	E = np.load (args.early_model)
	L = np.load (args.later_model)	
	logging.info ("Load embeddings from file ... done")

	# align the two matrices
	X1, X2, C = alignTwoModels (E, L, early_vocab, later_vocab)

	# row normalize the matrices	
	X1 = normalize (X1, axis=1, norm="l2")
	X2 = normalize (X2, axis=1, norm="l2")
	logging.info ("Align embeddings from file ... done")

	w2i, i2w = make_dict(C)

	# cultural shift calculation
	scores = dict ()
	for i,c in enumerate (w2i):
		scores[c] = cultural_shift (X1, X2, (w2i, i2w), c, k=50)

		if i % 1000 == 0:
			logging.info ("Words processed: {}/{}".format (i+1, len (C)))	

	logging.info ("Calculate innovativeness score ... done")

	# write the common vocab
	write_vocab (w2i, args.common_vocab_file)

	# write feature scores
	write_vocab (scores, args.features_file)
	logging.info ("Write features to file ... done")
	
if __name__ == "__main__":
	main (getArgs ())
