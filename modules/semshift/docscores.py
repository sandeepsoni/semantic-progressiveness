import numpy as np
import scipy

class Scorer (object):
	def __init__ (self, early_model, later_model, word):
		""" constructor for scoring with respect to the given models and the word

		Args:
			early_model (:obj: model): embeddings from early documents.
			later_model (:obj: model): embeddings from later documents.
			word (:obj: str): the word
		"""
		self.word = word
		w2i, i2w = early_model.index
		sim_early = np.dot (early_model.C, early_model.W[w2i[word]])
		sim_later = np.dot (later_model.C, later_model.W[w2i[word]])
		z_early = scipy.special.logsumexp (sim_early)
		z_later = scipy.special.logsumexp (sim_later)

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

class EmdsModel (object):
	def __init__ (self, C, W, index):
		self.C = C
		self.W = W
		self.index = index
