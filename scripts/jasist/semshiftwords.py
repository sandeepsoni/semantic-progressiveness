#import os
#import sys
import numpy as np
import argparse
from scipy.linalg import orthogonal_procrustes

import similarity_measures

def readArgs ():
	parser = argparse.ArgumentParser (description="Semantic shift scores")
	parser.add_argument ("--early-file", required=True, type=str, help="file containing the embeddings in the early period")
	parser.add_argument ("--later-file", required=True, type=str, help="file containing the embeddings in the later period")
	parser.add_argument ("--vocab-file", required=True, type=str, help="file containing the common vocabulary")
	parser.add_argument ("--scores-file", required=True, type=str, help="file containing the word and their scores")
	args = parser.parse_args ()
	return args

def readEmdsFromFile (filename):
	w2i, i2w = dict (), dict ()
	embeddings = list ()
	with open (filename) as fin:
		for i, line in enumerate (fin):
			if i > 0:
				parts = line.strip().split()
				word, embedding = parts[0], np.array(parts[1:], dtype=float)
				w2i[word] = i-1
				i2w[i-1] = word
				embeddings.append (embedding)

	return np.array (embeddings), w2i, i2w

def get_common_vocab (idx1, idx2):
	common_vocab = idx1.keys() & idx2.keys()
	w2i = {w: i for i, w in enumerate (common_vocab)}
	i2w = {i: w for i, w in enumerate (common_vocab)}
	return w2i, i2w

def stripMat (mat, common, idx):
	indices = [idx[w] for w,i in sorted (common.items(), key=lambda x:x[1], reverse=False)]
	return mat[indices]

def align2Mats (M1, M2):
	R,_ = orthogonal_procrustes (M1, M2)
	return np.dot (M1, R), M2

def main (args):
	E, w2i_early, i2w_early = readEmdsFromFile (args.early_file)
	L, w2i_later, i2w_later = readEmdsFromFile (args.later_file)

	print (f"Read embedding from file ... done")

	w2i_common, i2w_common = get_common_vocab (w2i_early, w2i_later)

	with open (args.vocab_file, "w") as fout:
		for w,i in sorted (w2i_common.items(), key=lambda x:x[1], reverse=False):
			fout.write (f"{w},{i}\n")

	print (f"Create common vocabulary ... done")

	E_common = stripMat (E, w2i_common, w2i_early)
	L_common = stripMat (L, w2i_common, w2i_later)	

	E_opt, L_opt = align2Mats (E_common, L_common)
	
	print (f"Aligning embeddings after procrustes ... done")

	scores = dict ()
	for i,w in enumerate (w2i_common):
		scores[w] = similarity_measures.hamilton_local_score (w, (w2i_common, i2w_common), E_opt, L_opt, k=25)

		if (i+1) % 1000 == 0:
			print (f"Words processed: {i+1}")

	with open (args.scores_file, "w") as fout:
		for w, score in sorted (scores.items(), key=lambda x:x[1], reverse=True):
			fout.write (f"{w},{score}\n")

	print (f"Semantic shift scores ... done")

if __name__ == "__main__":
	main (readArgs ())
