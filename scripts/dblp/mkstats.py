import plac
import ujson
import os

UNIQ_KEY="id"

def writeIds (key, srcfile, tgtfile):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			fout.write ("{0}\n".format (js[key]))

def writeYear (key, srcfile, tgtfile):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			fout.write ("{0},{1}\n".format (js[UNIQ_KEY], js[key]))

def writeNAuthors (key, srcfile, tgtfile):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			fout.write ("{0},{1}\n".format (js[UNIQ_KEY], js[key]))

def writeAbstract (key, srcfile, tgtfile):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			abstract = js[key].replace("\r"," ").replace ("\n"," ")
			fout.write ("{0}\n".format (abstract))

def writeNIncites (key, srcfile, tgtfile):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			fout.write ("{0},{1}\n".format (js[UNIQ_KEY], js[key]))

def writeTokens (key, srcfile, tgtfile):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			tokens = " ".join (js[key])
			tokens = tokens.replace ("\r", " ").replace ("\n", " ")
			fout.write ("{0}\n".format (tokens.lower()))

def writeNOutcites (key, srcfile, tgtfile):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			fout.write ("{0},{1}\n".format (js[UNIQ_KEY], len(js[key])))

def writeNUniqs (key, srcfile, tgtfile):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			tokens = js[key]
			uniqs = len({token.lower() for token in tokens})
			fout.write ("{0},{1}\n".format (js[UNIQ_KEY], uniqs))

def writeNTokens (key, srcfile, tgtfile):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			tokens = js[key]
			fout.write ("{0},{1}\n".format (js[UNIQ_KEY], len(tokens)))

@plac.annotations(
	srcfile=("file containing the corpus", "positional"),
	statsdir=("directory containing all the statistics", "positional"),
	key=("key in the json file (also becomes the extension of the target file)", "positional"),
	prefix=("prefix for the file", "option")
)
def main (srcfile, statsdir, key, prefix="dblp"):
	key_maps = {
		"id": ("id", writeIds),
		"year": ("year", writeYear),
		"nauthors": ("nauthors", writeNAuthors),
		"abstract": ("abstract", writeAbstract),
		"nincites": ("nincites", writeNIncites),
		"tokens": ("tokens", writeTokens),
		"noutcites": ("outcites", writeNOutcites),
		"nuniqs": ("tokens", writeNUniqs),
		"ntokens": ("tokens", writeNTokens)
	}

	tgtfile = os.path.join (statsdir, "{0}.{1}".format (prefix, key))
	fieldname, writeToFile = key_maps[key]
	writeToFile(fieldname, srcfile, tgtfile)

if __name__ == "__main__":
	plac.call (main)
