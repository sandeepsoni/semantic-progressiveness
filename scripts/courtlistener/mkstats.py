import plac
import ujson
import os
import heapq
import sys
from collections import defaultdict
import pandas as pd

if "../../" not in sys.path:
    sys.path.append ("../../")

from modules import constants
import logging

FORMAT="%(asctime)s : %(levelname)s : %(message)s"
logging.basicConfig (format=FORMAT, level=logging.INFO)

def json_iterator (filename):
	with open (filename) as fin:
		for line in fin:
			yield ujson.loads (line)

def mergeAndWriteMeta (filesdir, statsdir, jurs):
	iterables = [json_iterator (os.path.join (filesdir, jur + constants.JSONL_EXT)) for jur in jurs]
    
	OPS_FILE = os.path.join (statsdir, "ops.list")
	DATES_FILE = os.path.join (statsdir, "ops.dates")
	STATUS_FILE = os.path.join (statsdir, "ops.pubs")
	COURTS_FILE = os.path.join (statsdir, "ops.courts")
	TYPES_FILE = os.path.join (statsdir, "ops.types")

	linenum = 0    
	with open (OPS_FILE, "w") as ops_out, open (DATES_FILE, "w") as dates_out, open (STATUS_FILE, "w") as status_out, open(COURTS_FILE, "w") as courts_out, open(TYPES_FILE, "w") as types_out:
		merged = heapq.merge (*iterables, key=lambda x:x["date"])
		for js in merged:
			ops_out.write ("{0}\n".format (js["opid"]))
			dates_out.write ("{0},{1}\n".format (js["opid"], js["date"]))
			status_out.write ("{0},{1}\n".format (js["opid"], js["isapub"]))
			courts_out.write ("{0},{1}\n".format (js["opid"], js["court"]))
			types_out.write ("{0},{1}\n".format (js["opid"], js["type"])) 
			linenum += 1
			if linenum % constants.LAKH == 0: logging.info ("Processed and wrote {0} lines".format (linenum))
	
	logging.info ("Finished and wrote {0} lines".format (linenum))

def mergeAndWriteDocs (filesdir, statsdir, jurs):
	iterables = [json_iterator(os.path.join (filesdir, jur + ".tokenized" + constants.JSONL_EXT)) for jur in jurs]

	LENGTH_FILES = [os.path.join (statsdir, x) for x in ["ops.nuniqs", "ops.ntokens"]]
	DOCS_FILE = os.path.join (statsdir, "ops.docs")
	TEXTS_FILE = os.path.join (statsdir, "ops.texts")

	linenum = 0    
	with open (LENGTH_FILES[0], "w") as nuniqs_out, open (LENGTH_FILES[1], "w") as ntokens_out, open (DOCS_FILE, "w") as docs_out, open (TEXTS_FILE, "w") as texts_out:
		merged = heapq.merge (*iterables, key=lambda x:x["date"])
		for js in merged:
			text = js["text"].replace ("\r", "").replace("\n","")
			tokens = " ".join (js["tokens"])
			ntokens = len (js["tokens"])
			nuniqs = len (set (js["tokens"]))
			texts_out.write ("{0}\n".format (ujson.dumps ({"opid": js["opid"], "text": text})))
			docs_out.write ("{0}\n".format (ujson.dumps ({"opid": js["opid"], "doc": tokens})))
			nuniqs_out.write ("{0},{1}\n".format (js["opid"], nuniqs))
			ntokens_out.write ("{0},{1}\n".format (js["opid"], ntokens))
			linenum += 1
			if linenum % constants.LAKH == 0: logging.info ("Processed and wrote {0} lines".format (linenum))
	
	logging.info ("Finished and wrote {0} lines".format (linenum))

def readCitationNetAsDicts (filename):
	indict = defaultdict (int)
	outdict = defaultdict (int)

	df = pd.read_csv (filename, sep=",")

	froms = df["citing_opinion_id"].values
	tos = df["cited_opinion_id"].values

	for i in range (len(froms)):
		outdict[froms[i]] += 1
		indict[tos[i]] += 1

	return indict, outdict

def writeCitationStats (statsdir, citesfile):
	OPS_FILE = os.path.join (statsdir, "ops.list")
	ind_dict, outd_dict = readCitationNetAsDicts(citesfile)
	
	IND_FILE = os.path.join (statsdir, "ops.ind")
	OUTD_FILE = os.path.join (statsdir, "ops.outd")

	with open (OPS_FILE) as fin, open(IND_FILE, "w") as indout, open (OUTD_FILE, "w") as outdout:
		for line in fin:
			op = int(line.strip())
			indout.write ("{0},{1}\n".format (op, ind_dict[op]))
			outdout.write ("{0},{1}\n".format (op, outd_dict[op]))

def readFile (filename):
	with open (filename) as fin:
		lines = [line.strip() for line in fin]
	return lines

@plac.annotations (
	filesdir=("files directory", "positional"),
	statsdir=("stats directory", "positional"),
	jursfile=("jurisdictions file", "positional"),
	citesfile=("citations file", "positional")
)
def main (filesdir, statsdir, jursfile, citesfile):
	os.makedirs (statsdir, exist_ok=True)
	jurs = readFile (jursfile)

	## first phase: write metadata stats
	logging.info ("Begin writing metadata stats")
	mergeAndWriteMeta(filesdir, statsdir, jurs)
	logging.info ("Done writing metadata stats")

	## second phase: write citation stats
	logging.info ("Begin writing citation stats")
	writeCitationStats (statsdir, citesfile)
	logging.info ("Done writing citation stats")

	## third phase: write document stats
	logging.info ("Begin writing document stats")
	mergeAndWriteDocs (filesdir, statsdir, jurs)
	logging.info ("Done writing document stats")

if __name__ == "__main__":
	plac.call (main)
