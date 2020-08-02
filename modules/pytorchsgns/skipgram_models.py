import torch
import torch.nn as nn

class SkipGram (nn.Module):
	def __init__ (self, vocab_size, embed_dims):
		super (SkipGram, self).__init__ ()
		self.embeddings = nn.Embedding (vocab_size, embed_dims)
		self.m = torch.nn.LogSigmoid()

	def forward (self, input_word, output_word, sign):
		"""
		:input_word: tensor (the input word, called target or the focus)
		:output_words: tensor (the output word, called the context)
		"""
		input_embedding = self.embeddings(input_word).squeeze (0)
		output_embedding = self.embeddings(output_word).squeeze (0)
		score = self.m (sign * torch.dot (input_embedding, output_embedding))
		return score
