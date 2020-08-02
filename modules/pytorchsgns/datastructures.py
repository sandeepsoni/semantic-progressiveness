import numpy as np

class Vocab (object):
	def __init__ (self, w2i, i2w, counts):
		self.w2i = w2i
		self.i2w = i2w
		self.counts = counts

	def subsample (self, sampling=0.00001, ns_exponent=0.75):
		wf = np.array([self.counts[word] for word in self.w2i])
		wf = wf / wf.sum()
		ws = 1 - np.sqrt(sampling / wf)
		ws = np.clip(ws, 0, 1)

		ws = np.power(ws,ns_exponent)
		ws = ws / ws.sum() 
		
		self.counts = {word:ws[i] for i, word in enumerate (self.w2i)} 
