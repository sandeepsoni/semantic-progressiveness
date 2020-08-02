import plac
import pandas as pd
import ujson
import os
import logging
import numpy as np
import pandas as pd

FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig (format=FORMAT, level=logging.INFO)
UNK = "UNK"

def scoredist (filename):
	scores = list ()
	with open (filename) as fin:
		for i, line in enumerate (fin):
			js = ujson.loads (line)
			scores.extend([item["score"] for item in js["scores"]])

	progressives = np.array (scores)
	return scores

def readSemFeats (filename, percentiles=[99, 95, 90, 50], check_every=1000000, verbose=False):
	records = list ()
	header = ["nprog", "nreg", "max_prog", "max_prog_word", "max_reg", "max_reg_word"]
	header += ["nprog{0}".format (percentile) for percentile in percentiles]
	header += ["nreg{0}".format (percentile) for percentile in percentiles]

	scores = scoredist (filename)
	prog_scores_to_beat = np.percentile(scores, q=np.array(percentiles))
	reg_scores_to_beat = np.percentile (scores, q=100 - np.array(percentiles))

	with open (filename) as fin:
		for i, line in enumerate (fin):
			js = ujson.loads (line)
			items = [(item["score"], item["word"]) for item in js["scores"]]

			nprog = sum([1 for item in items if item[0] > 0]) 
			nreg = sum([1 for item in items if item[0] < 0])
			npercentiles = list ()
			if nprog > 0 or nreg > 0:
				max_prog, max_prog_word = max (items, key=lambda x:x[0])
				max_reg, max_reg_word = min (items, key=lambda x:x[0])
				npercentiles.extend ([len([s for s,_ in items if s >= score_to_beat]) 
									  for score_to_beat in prog_scores_to_beat])

				npercentiles.extend ([len([s for s,_ in items if s <= score_to_beat]) 
									  for score_to_beat in reg_scores_to_beat])

			else:
				max_prog, max_reg = -np.inf, -np.inf
				max_prog_word, max_reg_word = UNK, UNK
				npercentiles.extend (2*len(percentiles)*[-np.inf])

			records.append ([nprog, nreg, max_prog, max_prog_word, max_reg, max_reg_word] + npercentiles)
			if verbose and (i+1) % check_every == 0:
				logging.info ("Records processed: {0}".format (i+1))

	df = pd.DataFrame (records, columns=header)
	return df

@plac.annotations (
	srcdir=("the source directory with all the files", "positional"),
	tgtfile=("the target file", "positional"),
	docid=("the document id", "option"),
	indeg=("indegree of the document", "option"),
	outdeg=("outdegree of the document", "option"),
	year=("year of the document", "option"),
	nuniqs=("the number of types per document", "option"),
	ntokens=("the number of tokens per document", "option"),
	bows=("the BoW scores per document", "option"),
	sems=("the semantic feature scores per document", "option")
)
def main (srcdir,
		  tgtfile,
		  docid="ops.list", 
		  indeg="ops.ind",
		  outdeg="ops.outd",
		  year="ops.dates",
		  nuniqs="ops.nuniqs",
		  ntokens="ops.ntokens",
		  bows="ops.bowscores",
		  sems="ops.1K.feats_manual.semscores"):

	df_ids = pd.read_csv (os.path.join (srcdir, docid), sep=",", header=None, names=["docid"])
	logging.info ("Read IDs ... done")
	df_indeg = pd.read_csv (os.path.join (srcdir, indeg), sep=",", header=None, names=["docid", "indeg"])
	df_outdeg = pd.read_csv (os.path.join (srcdir, outdeg), sep=",", header=None, names=["docid", "outdeg"])	
	logging.info ("Read citation stats ... done")
	df_year = pd.read_csv (os.path.join (srcdir, year), sep=",", header=None, names=["docid", "date"])
	df_year.loc[:, "year"] = df_year["date"].str.split(pat="-").map(lambda x: x[0])
	logging.info ("Read metadata stats ... done")	
	df_nuniqs = pd.read_csv (os.path.join (srcdir, nuniqs), sep=",", header=None, names=["docid", "nuniqs"])
	df_ntokens = pd.read_csv (os.path.join (srcdir, ntokens), sep=",", header=None, names=["docid", "ntokens"])
	df_bows = pd.read_csv (os.path.join (srcdir, bows), sep=",", header=None, names=["bows"])
	logging.info ("Read document stats ... done")	

	df_sems = readSemFeats (os.path.join (srcdir, sems))
	logging.info ("Read progressiveness stats ... done")	

	df = pd.concat([df_ids["docid"], 
					df_indeg["indeg"],
					df_outdeg["outdeg"],
					df_year["year"],
					df_nuniqs["nuniqs"],
					df_ntokens["ntokens"],
					df_bows["bows"]], 
					axis=1)

	logging.info ("Concatenate all except progressiveness ... done")

	df = pd.concat ([df,df_sems], axis=1)
	logging.info ("Concatenate progressiveness ... done")
	df.to_csv (os.path.join (srcdir, tgtfile), sep=",", index=False)
	logging.info ("Write to file ... done")

if __name__ == "__main__":
	plac.call (main)

