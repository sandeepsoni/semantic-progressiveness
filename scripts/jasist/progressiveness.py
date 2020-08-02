import argparse
import numpy as np
from scipy.special import logsumexp
import scipy

class Scorer (object):
	def __init__ (self, word, early_input, early_output, later_input, later_output, ind):
		self.word = word
		sim_early = np.dot (early_output, early_input[ind])
		sim_later = np.dot (later_output, later_output[ind])

		z_early = logsumexp (sim_early)
		z_later = logsumexp (sim_later)

		self.simdiff = sim_later - sim_early
		self.zdiff = z_later - z_early
	
	def score (self, doc, w2i, window_size=10):
		"""score a given document with respect to the word

		Args:
			doc (:obj: list): document as a list of tokens.
			w2i (:obj: dict): mapping between words to array position.
			window_size (int, optional): the size of the context window (default=10).

		Returns:
			float: document score wrt `self.word`, and the initialized models.

		Precondition:
			1. It has been determined that the document contains the word.

		Todo:
			1. test if the scoring function is correct using several test cases.
		"""
		def make_contexts_bow (doc, word, w2i, k=10):
			"""makes a bow vector of contexts around the target word

			Args:
				doc (:obj: list): document as a list of tokens.
				word(:obj: str): the target word
				w2i(:obj: dict): maps any word to a position.
				k(int, optional): the window size around `word` (default=10)
			"""
			doc = [tok for tok in doc if tok.isalpha()]
			last_token_index = len(doc) - 1
			word_positions = [i for i, token in enumerate (doc) if token == word]
			spans = [(max(0, pos-k), min(last_token_index, pos+k)) for pos in word_positions]
			bow = np.zeros (len(w2i))

			for i, span in enumerate (spans):
				start, end = span
				for pos in range (start, end+1):
					if not pos == word_positions[i]:
						if doc[pos] in w2i:
							bow[w2i[doc[pos]]] += 1

			return bow

		contexts_bow = make_contexts_bow (doc, self.word, w2i, k=window_size)
		cooccurrence_factor = np.dot (contexts_bow, self.simdiff)
		normalization_factor = sum(contexts_bow) * self.zdiff
		score = cooccurrence_factor - normalization_factor
		return score

def readEmdsFromFile (inputs_filename, outputs_filename):
	w2i, i2w = dict (), dict ()
	input_embeddings = list ()
	output_embeddings = list ()
	with open (inputs_filename) as fin1, open (outputs_filename) as fin2:
		for i, line in enumerate (fin1):
			if i > 0:
				parts = line.strip().split()
				word, embedding = parts[0], np.array(parts[1:], dtype=float)
				w2i[word] = i-1
				i2w[i-1] = word
				input_embeddings.append (embedding)

		for i, line in enumerate (fin2):
			if i > 0:
				parts = line.strip().split()
				word, embedding = parts[0], np.array (parts[1:], dtype=float)
				output_embeddings.append (embedding)

	return np.array (input_embeddings), np.array (output_embeddings), w2i, i2w

def readArgs ():
	parser = argparse.ArgumentParser ("Progressiveness calculation script")
	parser.add_argument ("--early-emds-file", type=str, required=True, help="early input embeddings")
	parser.add_argument ("--early-contexts-file", type=str, required=True, help="early output embeddings")
	parser.add_argument ("--later-emds-file", type=str, required=True, help="later input embeddings")
	parser.add_argument ("--later-contexts-file", type=str, required=True, help="later output embeddings")
	parser.add_argument ("--changes-file", type=str, required=True, help="changes file")
	parser.add_argument ("--docs-file", type=str, required=True, help="document content file")
	parser.add_argument ("--output-file", type=str, required=True, help="output file")
	args = parser.parse_args ()
	return args

def progressiveness_scores (early_emds, later_emds, e_w2i, l_w2i, changes_file, docs_file):
	e_input_emds, e_output_emds = early_emds
	l_input_emds, l_output_emds = later_emds


	common = set ([w for w in e_w2i]) & set ([w for w in l_w2i])
	common = [w for w in common]
	e_input_emds = e_input_emds[[e_w2i[w] for w in common],:]
	e_output_emds = e_output_emds[[e_w2i[w] for w in common],:]

	l_input_emds = l_input_emds[[l_w2i[w] for w in common], :]
	l_output_emds = l_output_emds[[l_w2i[w] for w in common], :]

	idx, iidx = {w: i for i,w in enumerate (common)}, {i: w for i,w in enumerate (common)}

	changes = list ()
	with open (changes_file) as fin:
		for i,line in enumerate (fin):
			if i > 0:
				parts = line.strip().split(",")
				changes.append (parts[1])

	change_set = set (changes)
	scorers = {change: Scorer (change, e_input_emds, e_output_emds, l_input_emds, l_output_emds, idx[change]) for change in change_set if not change == "UNK"}

	scores = list ()
	with open (docs_file) as fin:
		for i, line in enumerate (fin):
			if changes[i] == "UNK" or changes[i] not in scorers:
				scores.append (-np.inf)
			else:
				scores.append (scorers[changes[i]].score (line.strip().split(), idx))

			if (i+1) % 100000 == 0:
				print (f"{i+1} documents processed")

	return scores

def write_scores (scores, filename):
	with open (filename, "w") as fout:
		for score in scores:
			fout.write (f"{score}\n")

def main (args):
	early_input_emds, early_output_emds, early_w2i, early_i2w = readEmdsFromFile (args.early_emds_file, args.early_contexts_file)
	later_input_emds, later_output_emds, later_w2i, later_i2w = readEmdsFromFile (args.later_emds_file, args.later_contexts_file)

	scores = progressiveness_scores ((early_input_emds, early_output_emds), (later_input_emds, later_output_emds), early_w2i, later_w2i, args.changes_file, args.docs_file)
	write_scores (scores, args.output_file)

if __name__ == "__main__":
	main (readArgs ())
