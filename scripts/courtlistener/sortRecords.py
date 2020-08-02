import ujson
import plac
import os
import sys

if "../../" not in sys.path:
	sys.path.append ("../../")

from modules import constants

def sortByDate (dirname, jur):
	with open (os.path.join (dirname, jur + constants.JSONL_EXT)) as fin:
		jsons = [ujson.loads (line) for line in fin]

	with open (os.path.join (dirname, jur + constants.JSONL_EXT), "w") as fout:
		for js in sorted (jsons, key=lambda x:x["date"]):
			fout.write (ujson.dumps (js) + constants.NL)

@plac.annotations(
	filesdir=("directory from which files are read and written to", "positional"),
	jurname=("the jurisdiction name", "positional")
)
def main (filesdir, jurname):
	sortByDate (filesdir, jurname)	

if __name__ == "__main__":
	plac.call(main)
