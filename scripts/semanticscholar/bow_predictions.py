import numpy as np
import os
import plac

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

MILLION = 1000000
STATS_DIR = "/hg191/corpora/academic-data/semantic-scholar/stats/"
INDEG_FILE = os.path.join (STATS_DIR, "abs.ind")
DOCS_FILE = os.path.join (STATS_DIR, "abs.docs")
LINENUMS_FILE = os.path.join (STATS_DIR, "abs.bow-linenums")

def readIndex (filename):
	indices = set ()
	with open (filename) as fin:
		for line in fin:
			indices.add (line.strip())

	return indices

def readCorpus (filename, indices, verbose=False):
	corpus = list ()
	for i, line in enumerate (fin):
		if i in indices:
			corpus.append (line.strip())

		if verbose and i % MILLION == 0:
			print ("{0}, lines processed: {1}".format (filename, i))

	return corpus

def readGroundTruth (filename, indices, verbose=False):
	indegrees = list ()
	for line in fin:
		indegrees.append (int(line.strip().split(",")[1]))

	return indegrees

@plac.annotations (
	predictionsfile=("the predictions file", "positional"),
	
)
def main (predictionsfile):
	indices = readIndex (LINENUMS_FILE)
	corpus = readCorpus (DOCS_FILE, indices, verbose=True)
	indegrees = readGroundTruth (INDEG_FILE, indices, verbose=True)
	y = np.array ([indegrees[i] for i in range (len(indegrees)) if i in indices])
	K = 25000

	pipeline = Pipeline ([(
		("vect", CountVectorizer ()),
		("regr", LinearRegression())
	)])
	
	parameters = {
		"vect__max_features": (25000, 50000, 75000, 100000),
		"vect__min_tf": (10,),
		"vect__min_df": (3,)
	}

	grid_search = GridSearchCV (pipeline, parameters, cv=5, n_jobs=4, verbose=1)
	grid_search.fit(corpus[:K], np.log(y[:K] + 1))

	



if __name__ == "__main__":
	plac.call (main)
