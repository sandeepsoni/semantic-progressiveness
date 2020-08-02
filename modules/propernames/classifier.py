import torch
import torch.nn as nn
import torch.nn.functional as F

class TwoLayerNet (nn.Module):
	def __init__ (self, input_dim, hidden_dim, output_dim):
		super (TwoLayerNet, self).__init__()
		self.linear1 = nn.Linear (input_dim, hidden_dim)
		self.linear2 = nn.Linear (hidden_dim, input_dim) 

	def forward (self, x, f):
		h = f (self.linear1(x))
		y = self.linear2(h)
		return F.log_softmax(y, dim=1)	
