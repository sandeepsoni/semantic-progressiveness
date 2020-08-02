import ujson
import plac
import glob
import os

def filterJSON (injs, opinion_id, court, keys=[]):
	outjs = {}
	outjs["id"] = int(opinion_id)
	outjs["court"] = court
	for key in keys:
		outjs[key] = injs[key]

	return outjs

@plac.annotations (
	srcdir=("directory containing input files", "positional"),
	tgtdir=("directory containing output files", "positional")
)
def main (srcdir, tgtdir):
	court = os.path.basename (os.path.dirname(srcdir))
	outFile = os.path.join (tgtdir, "{0}.jsonl".format (court))
	with open (outFile, "w") as fout:
		for filename in glob.glob (os.path.join (srcdir, "*.json")):
			opid = os.path.basename (os.path.splitext (filename)[0])
			f = open (filename)
			injs = ujson.load(f)
			f.close()
			js = filterJSON(injs, opid, court, keys=["judges", "precedential_status", "date_filed", "case_name", "absolute_url"])
			fout.write (ujson.dumps (js) + "\n")

if __name__ == "__main__":
	plac.call (main)
