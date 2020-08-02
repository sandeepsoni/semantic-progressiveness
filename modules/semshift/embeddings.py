import gensim
from gensim.models.callbacks import CallbackAny2Vec

import sys

class TrainedModel (object):
	""" Hamilton et al. (2016): train SGNS model on slices of the corpora sorted by time;
		then align the embeddings from different slices """
	
	def __init__ (self, filename, normalize=True):
		self.m = gensim.models.Word2Vec.load (filename)
		self.m.wv.init_sims (replace=normalize)
