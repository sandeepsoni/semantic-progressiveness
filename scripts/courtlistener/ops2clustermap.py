import ujson
import glob
import os
import plac

import sys
if not os.path.abspath("../../") in sys.path:
	sys.path.append (os.path.abspath ("../../"))

from modules import constants

def extract_from_opinions (filename):
	with open (filename) as fin:
		js = ujson.load (fin)
	cnum = js["cluster"].strip("/").split("/")[-1]
	op = js["absolute_url"].strip("/").split("/")[1]
	
	return op, cnum 

def extract_from_clusters (filename):
	with open (filename) as fin:
		js = ujson.load (fin)

	op  = js["absolute_url"].strip("/").split("/")[1]
	subs = ",".join([op.strip("/").split("/")[-1] for op in js["sub_opinions"]])
	
	return op, subs

@plac.annotations (
	jur=("jurisdiction", "positional"),
	tgtdir=("place the file in this directory", "positional")
)
def main (jur, tgtdir):
	with open (os.path.join (tgtdir, "{0}.tsv".format (jur)), "w") as fout:
		fout.write ("\t".join (["opfid", "clid", "opid", "clfileexists", "subops"]) + "\n")
		for filename in glob.glob (os.path.join (constants.OPINIONS_DIR, jur, "*.json")):
			fid = os.path.basename (filename.split(".")[0])
			opid1, cnum = extract_from_opinions (filename)
			cluster_filename = os.path.join (constants.CLUSTERS_DIR, jur, cnum+".json")
			if os.path.exists (cluster_filename):
				opid2, subops = extract_from_clusters (cluster_filename)
				assert (opid1 == opid2)
				fout.write ("\t".join([fid, cnum, opid1, str(True), subops]) + "\n")
			else:
				fout.write ("\t".join([fid, cnum, opid1, str(False)]) + "\n")

if __name__ == "__main__":
	plac.call (main)
