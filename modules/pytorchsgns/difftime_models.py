import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import numpy as np
import math

class ModifiedLinearLayer (nn.Module):
	def __init__ (self, in_features, mid_features, out_features, bias=True):
		super(ModifiedLinearLayer, self).__init__()
		self.in_features = in_features
		self.mid_features = mid_features
		self.out_features = out_features
		self.weight = nn.parameter.Parameter (torch.Tensor (in_features, mid_features, out_features))
		if bias:
			self.bias = nn.parameter.Parameter (torch.Tensor (in_features, mid_features))
		else:
			self.register_parameter ("bias", None)
		self.reset_parameters ()

	def reset_parameters (self):
		nn.init.kaiming_uniform_ (self.weight, a=math.sqrt (5))
		if self.bias is not None:
			fan_in, _ = nn.init._calculate_fan_in_and_fan_out(self.weight)
			bound = 1 / math.sqrt(fan_in)
			nn.init.uniform_(self.bias, -bound, bound)

	def forward (self, input):
		trans = torch.matmul (self.weight, input) + self.bias
		return trans

	def extra_repr(self):
		return 'in_features={}, mid_features={}, out_features={}, bias={}'.format(
			self.in_features, self.mid_features, self.out_features, self.bias is not None
		)
class WordComponent (nn.Module):
	def __init__ (self, vocab_size, embed_dims):
		super (WordComponent, self).__init__ ()
		self.embeddings = nn.Embedding (vocab_size, embed_dims)

	def forward (self, input_word):
		return self.embeddings(input_word).squeeze (0)

class TimeComponent (nn.Module):
	def __init__ (self, l1size, l2size):
		super (TimeComponent, self).__init__ ()
		self.linear1 = nn.Linear (1, l1size)
		self.linear2 = nn.Linear (l1size, l2size)

	def forward (self, input_time):
		h1 = torch.tanh(self.linear1(input_time))
		return torch.tanh(self.linear2(h1)).squeeze (0)

class DiffTime (nn.Module):
	def __init__ (self, mod_linear_sizes, time_component_sizes, final_layer_sizes, vocab_size, embed_dims):
		super (DiffTime, self).__init__ ()	

		### The dimensions of different layers.
		input_size, mid_size = mod_linear_sizes 
		l1size, l2size = time_component_sizes
		final_input_size, final_output_size = final_layer_sizes

		### All the different layers.
		self.mod_linear = ModifiedLinearLayer (input_size, mid_size, embed_dims)
		self.tc = TimeComponent (l1size, l2size)
		
		# WordComponent is just an embedding layer: we have two such modules
		# because we want to have different embeddings for word and context vectors.
		self.input_wc = WordComponent (vocab_size, embed_dims)
		self.output_wc = WordComponent (vocab_size, embed_dims)
		self.final_layer = nn.Linear (final_input_size, final_output_size)
		self.m = torch.nn.LogSigmoid ()

	def forward (self, input_word, output_word, time, sign):
		transw = self.mod_linear (self.input_wc.forward (input_word))
		transc = self.mod_linear (self.output_wc.forward (output_word))

		timevec = self.tc.forward(time)

		h3_input = torch.matmul (transw, timevec)
		h3_output = torch.matmul (transc, timevec)
		
		usew = self.final_layer.forward (h3_input)
		usec = self.final_layer.forward (h3_output)

		score = self.m (sign * torch.dot (usew, usec))
		return score
