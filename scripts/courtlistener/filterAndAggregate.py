""" Make an easy to use processed corpus file of all records.
"""

import plac
import ujson
import sys
import os
import glob
import shutil
import numpy as np
from bs4 import BeautifulSoup

if "../../" not in sys.path:
	sys.path.append ("../../")

from modules import constants

def readJSONFromFile (filename):
	with open (filename) as fin:
		js = ujson.load (fin)

	return js

def parseFieldFromURL (url, fieldnum):
	return url.strip("/").split("/")[fieldnum]

def meetsCondition (opinion, cluster):
	hastext_ashtml = opinion.get ("html_with_citations", None) is not None and len(opinion.get("html_with_citations")) > 0
	hastext_astext = opinion.get ("plain_text", None) is not None and len (opinion.get ("plain_text")) > 0

	hastext = hastext_ashtml | hastext_astext

	op_fromopinion = parseFieldFromURL(opinion.get ("absolute_url"), 1)
	op_fromcluster = parseFieldFromURL(cluster.get ("absolute_url"), 1)

	opinion_matches = (op_fromopinion == op_fromcluster)

	return hastext and opinion_matches


def preprocess_text (opinion):
	hastext_ashtml = opinion.get ("html_with_citations", None) is not None and len(opinion.get("html_with_citations")) > 0
	hastext_astext = opinion.get ("plain_text", None) is not None and len (opinion.get ("plain_text")) > 0
	
	if hastext_ashtml:
		soup = BeautifulSoup (opinion.get("html_with_citations"), "html5lib")
		text = soup.get_text().replace ("\n", " ")
		return text 
	elif hastext_astext:
		text = opinion.get("plain_text")
		text = text.replace ("\n", " ")
		return text

def mergeRecord (opinion, cluster, jurname):
	common = {}

	common["opid"] = int (parseFieldFromURL (opinion.get ("absolute_url"), 1))
	common["pages"] = opinion.get ("page_count", -1)
	common["type"] = opinion.get ("type", "")
	common["clid"] = int (parseFieldFromURL (opinion.get("cluster"), -1))
	common["text"] = preprocess_text (opinion)
	
	common["blocked"] = cluster.get("blocked", False)
	common["case"] = cluster.get ("case_name", "")
	common["date"] = cluster.get ("date_filed", "")
	common["subops"] = list(map (lambda x:int(parseFieldFromURL(x, -1)), cluster["sub_opinions"]))
	common["court"] = jurname
	common["isapub"] = cluster.get("precedential_status", "UNK")	

	return common

def filterAndAggregate (jurname, filesdir):
	with open (os.path.join (filesdir, jurname+constants.JSONL_EXT), "w") as fout:
		for opinionfile in glob.glob (os.path.join (constants.OPINIONS_DIR, jurname, "*.json")):
			opjs = readJSONFromFile (opinionfile)
			cnum = parseFieldFromURL (opjs["cluster"], -1)
			clfile = os.path.join (constants.CLUSTERS_DIR, jurname, cnum+constants.JSON_EXT)
			cljs = readJSONFromFile (clfile)
			if meetsCondition (opjs, cljs):
				mergedjs = mergeRecord (opjs, cljs, jurname)
				fout.write (ujson.dumps (mergedjs) + constants.NL)	

@plac.annotations(
	filesdir=("directory in which files are created", "positional"),
	jurname=("jurisdiction", "positional")
)
def main (filesdir, jurname):
	filterAndAggregate (jurname, filesdir)

if __name__ == "__main__":
	plac.call (main)
