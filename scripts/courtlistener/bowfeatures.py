"""
Use the content of the document to predict the number of citations. A document can be represented as a bag of words. 

Instead of concatenating all the BoW features to the hand-selected features, we use the following strategy.

We get a sample of the corpus (eg. 1 million documents) and divide into training and test set. Train the best regression model and then make predictions for all documents in the corpus. Use this as a feature in the downstream regression.
"""

import numpy as np
import os
import ujson
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate, KFold
from sklearn.metrics import mean_squared_log_error

import plac
import logging

FORMAT = "%(asctime)s : %(levelname)s : %(message)s"
logging.basicConfig (format=FORMAT, level=logging.INFO)

def readDocuments (filename, lines):
	with open (filename) as fin:
		docs = list ()
		for i, line in enumerate (fin):
			if i in lines:
				docs.append (line.strip())
	
	return docs

def readCitations (filename, lines):
	with open (filename) as fin:
		ind = [float(line.strip().split(",")[1]) for i, line in enumerate (fin) if i in lines]
	return ind

def applyAndWritePredictions (vect, model, srcfile, tgtfile, batch_size=100000):
	minibatch = list ()
	rounds = 0

	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for i,line in enumerate (fin):
			doc = line.strip()
			minibatch.append (doc)
			if len(minibatch) == batch_size:
				X_hat = vect.transform (minibatch)
				yhat = np.exp(model.predict (X_hat)) - 1
				for pred in yhat:
					fout.write ("{0}\n".format (pred))
				fout.flush()
				logging.info ("[Round: {0}]: Total records processed={1}".format (rounds+1, (rounds+1) * len(minibatch)))
				minibatch = list ()
				rounds += 1

		if len (minibatch) > 0:
			X_hat = vect.transform (minibatch)
			yhat = np.exp(model.predict (X_hat)) + 1
			for pred in yhat:
				fout.write ("{0}\n".format (pred))
			fout.flush()
			logging.info ("[Round: {0}]: Total records processed={1}".format (rounds+1, (rounds) * 100000 + len(minibatch)))

	

@plac.annotations(
	tokensfile=("file containing document tokens per line", "positional"),
	citesfile=("file containing the citations of the document", "positional"),
	bowscoresfile=("file containing the scores after training a classifier", "positional"),
	ndocs=("the number of documents in the file", "positional", None, int),
	nsamples=("the number of documens in the sample to train", "option", None, int),
	seed=("the seed value for the random number generator", "option", None, float)
)
def main (tokensfile, citesfile, bowscoresfile, ndocs, nsamples=200000, seed=42):
	np.random.seed (seed)
	linenums = np.sort (np.random.choice(ndocs, nsamples, replace=False))
	linesset = set (linenums)

	docs = readDocuments (tokensfile, linesset)
	cites = readCitations (citesfile, linesset)
	
	assert (len(docs) == len (cites))

	logging.info ("Data read from file")
	indices = list (range (0, len(docs)))
	np.random.shuffle (indices)

	sample_cites = [cites[index] for index in indices]
	sample_docs = [ujson.loads(docs[index])["doc"] for index in indices]

	# Trained model
	count_vect = CountVectorizer(max_features=10000, min_df=3, max_df=0.9)
	X = count_vect.fit_transform (sample_docs)
	y = np.array (sample_cites)

	lm = LinearRegression ()
	lm.fit (X, np.log (y+1))	
	logging.info ("Trained BoW model")
	
	# Apply the model to every document.
	applyAndWritePredictions (count_vect, lm, tokensfile, bowscoresfile)

if __name__ == "__main__":
	plac.call (main)
