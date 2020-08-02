import gensim
import os
import numpy as np
import scipy

class TrainedModel(object):
	""" Hamilton et al. (2016) : train SGNS model on slices of the corpora sorted by time;
		then realign the embeddings from different slices """
	@classmethod
	def fromFiles (cls, filenames):
		models = [gensim.models.Word2Vec.load (filename) for filename in filenames]
		return TrainedModel (models)

	def __init__ (self, models):
		self.models = models

	def normalize (self):
		for model in self.models:
			model.wv.init_sims (replace=True)

	def getEmbeddings (self, using="target", vocab=None):
		""" get the learned embeddings

		Parameters
		----------
		using: str
			This parameter can take one of the following three values
			(a) target: use the normalized input embeddings only
			(b) context: use the normalized output embeddings only
			(c) average: use the average of input and output embeddings and then normalize

			For now, only the "target" option is working. To make the other options work,
			make sure `init_sims` is not called on the embeddings -- this will avoid 
			normalizing the vectors. After that the input embeddings are accessible using
			`word2vec.wv.vectors`, whereas the output embeddings are accessible using 
			`word2vec.trainables.syn1neg`

		vocab: set
			The vocabulary for which the embeddings are needed. If None, take the 
			intersection of the vocabularies from all the models.
		"""
		embeds = list ()

		if using == "context" or using == "average":
			raise NotImplementedError

		vocabs = [set (model.wv.vocab.keys()) for model in self.models]
		
		if vocab is None:
			common = list (set.intersection (*vocabs))
		else:
			common = list (vocab & set.intersection (*vocabs))

		idx = {w:i for i, w in enumerate (common)}
		iidx = {i:w for i, w in enumerate (common)}

		V = [iidx[i] for i in range (len (iidx))]
		for model in self.models:
			index = [model.wv.vocab[w].index for w in V]
			oldA = model.wv.vectors
			newA = np.array ([oldA[index] for i in index])
			embeds.append (newA)

		return embeds

	def realignAll (self, emds):
		final_emds = list ()
		for prev_emd, next_emd in zip (emds[:-1], emds[1:]):
			R,_ = scipy.linalg.orthogonal_procrustes (prev_emd, next_emd)
			final_emds.append (prev_emd.dot (R))

		final_emds.append (next_emd)
		return final_emds

	def realignTo (self, emd1, emd2):
		R,_ = scipy.linalg.orthogonal_procrustes (emd1, emd2)
		return emd1.dot (R)
