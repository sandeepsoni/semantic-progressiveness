import logging
from gensim.models.callbacks import CallbackAny2Vec

class EpochLogger(CallbackAny2Vec):
	""" Callback to log information about training """
	def __init__(self):
		self.epoch = 0
		self.prev_loss = 0
		self.losses = list ()

	def on_epoch_end(self, model):
		current_loss = model.get_latest_training_loss ()
		self.losses.append (current_loss - self.prev_loss)
		self.epoch += 1
		logging.info ("After epoch #{0}, loss={1}".format (self.epoch, self.losses[-1]))
		self.prev_loss = current_loss
