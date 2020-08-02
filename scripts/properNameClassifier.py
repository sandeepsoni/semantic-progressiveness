import numpy as np
from collections import Counter
from random import shuffle
from sklearn.metrics import accuracy_score, roc_auc_score

import sys
sys.path.append ("../modules")
from propernames.classifier import TwoLayerNet

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.manual_seed(1)

def readAnnotations (filename):
	with open (filename) as fin:
		sample = [line.strip() for line in fin]

	return sample

def prepareData (sample, labelmap):
	positives = [candidate.strip("+") for candidate in sample if candidate.startswith ("+")]
	negatives = [candidate for candidate in sample if not candidate.startswith ("+")]

	assert (len (positives) + len (negatives) == len (sample))

	sample = positives + negatives
	shuffle (sample)

	data = [(candidate, labelmap[int (candidate in positives)]) for candidate in sample]
	return data

def splitData (data, split_proportions):
	s = sum (split_proportions)
	unit_size = len(data) / s
	train_data = data[0:split_proportions[0] * unit_size]
	dev_data = data[split_proportions[0] * unit_size: (split_proportions[0] + split_proportions[1]) * unit_size]
	test_data = data[(split_proportions[0] + split_proportions[1]) * unit_size: s*unit_size]
	return train_data, dev_data, test_data

def use_embeddings (instance, emds, mapping):
	"""Takes an instance and coverts into a vector"""
	vec = torch.Tensor (emds[mapping[instance]])
	return vec.view(1,-1)

def make_target (label, mapping):
	"""Takes a label and coverts it into a categorical variable"""
	return torch.LongTensor([mapping[label]])

def train (instances, emds, idx, model, loss_function, optimizer, nEpochs):
	for epoch in range (nEpochs):
		for instance, label in instances:
			model.zero_grad ()
			src = use_embeddings (instance, emds, idx)
			tgt = make_target (label, labels_map)
			

@plac.annotations (
	annotationsfile=("file with annotated data", "positional"),
	vocabfile = ("file containing the vocabulary (used as test set)", "positional"),
	embeddingsfile = ("file containing the embeddings", "positional")
)
def main (annotationsfile, vocabfile, embeddingsfile):
	input_dim=100
	label_size = 2
	labels_map = {"Name":1, "NonName":0}
	iLabels_map = {1:"Name", 0:"NonName"}
	nEpochs = 25

	data = prepareData (readAnnotations (annotationsfile), iLabels)
	train_data, dev_data, test_data = splitData (data, (5,2,1))
	train_truth = list (map (lambda x:labels_map[x[1]], train_data))
	dev_truth = list (map (lambda x:labels_map[x[1]], dev_data))
	test_truth = list (map (lambda x:labels_map[x[1]], test_data))

	input_dim = embeds_dim
	model = TwoLayerNet (input_dim, input_dim, label_size)

	loss_function = nn.NLLLoss()
	optimizer = optim.SGD (model.parameters (), lr=0.1)
	
	model, losses = train (train_data, emds, idx, model, loss_function, optimizer, nEpochs) #TODO read embeddings
	


loss_function = nn.NLLLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

if __name__ == "__main__":
	plac.call (main)
