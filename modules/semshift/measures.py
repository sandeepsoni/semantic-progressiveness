import numpy as np
import gensim

class HamiltonMeasures (object):

	@staticmethod
	def linguistic_drift (before, after, word):
		""" Hamilton et al. (2016) proposed a measure for linguistic drift,
			which is simply the cosine distance between the embeddings of 
			a word before and after

			Parameters
			----------

			:before: gensim.models.Word2Vec
				embeddings model

			:after: gensim.models.Word2Vec
				embeddings model

			:word: str
				word for which the measure is to be calculated

			Pre-requisites
			--------------
			Both the gensim models should be comparable i.e according to Hamilton et al.
			they should be aligned.
		"""
		if word not in before.wv.vocab or word not in after.wv.vocab:
			return 0

		vec1 = before.wv[word] / np.linalg.norm (before.wv[word])
		vec2 = after.wv[word] / np.linalg.norm (after.wv[word])
	
		sim = vec1.dot (vec2)
		return 1-sim


	def cultural_shift (before, after, word, k=10):
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

			:before,after: gensim.models.Word2Vec
				embeddings models

			:word: str
				word for which the measure is to be calculated
		
			:k: int
				the number of nearest neighbors

		"""
		if word not in before.wv.vocab or word not in after.wv.vocab:
			return 0

		nn1 = before.wv.most_similar (word, topn=k)
		nn2 = after.wv.most_similar (word, topn=k)
		common = set ([w for w,_ in nn1]) | set ([w for w,_ in nn2])

		sim1 = np.array ([before.wv.similarity (w, word) for w in common])
		sim2 = np.array ([after.wv.similarity (w, word) for w in common])

		sim = np.dot (sim1, sim2)/(np.linalg.norm (sim1) * np.linalg.norm (sim2))
		return 1-sim
