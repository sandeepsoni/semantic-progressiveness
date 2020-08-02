import plac
import ujson
import os

UNIQ_KEY="filename"

def writeIds (key, srcfile, tgtfile, start=1827, end=1922):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			if js["year"] >= start and js["year"] <= end:
				fout.write ("{0}\n".format (js[key]))

def writeNewspapers (key, srcfile, tgtfile, start=1827, end=1922):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			if js["year"] >= start and js["year"] <= end:
				fout.write ("{0},{1}\n".format (js[UNIQ_KEY], js[key]))

def writeYear (key, srcfile, tgtfile, start=1827, end=1922):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			if js["year"] >= start and js["year"] <= end:
				fout.write ("{0},{1}\n".format (js[UNIQ_KEY], js[key]))

def writeText (key, srcfile, tgtfile, start=1827, end=1922):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			if js["year"] >= start and js["year"] <= end:
				text = js[key].replace("\r"," ").replace ("\n"," ")
				fout.write ("{0}\n".format (text))

def writeTokens (key, srcfile, tgtfile, start=1827, end=1922):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			if js["year"] >= start and js["year"] <= end:
				tokens = " ".join (js[key])
				tokens = tokens.replace ("\r", " ").replace ("\n", " ")
				fout.write ("{0}\n".format (tokens.lower()))

def writeUncasedTokens (key, srcfile, tgtfile, start=1827, end=1922):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			if js["year"] >= start and js["year"] <= end:
				tokens = " ".join (js[key])
				tokens = tokens.replace ("\r", " ").replace ("\n", " ")
				fout.write ("{0}\n".format (tokens))

def writeNUniqs (key, srcfile, tgtfile, start=1827, end=1922):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			if js["year"] >= start and js["year"] <= end:
				tokens = js[key]
				uniqs = len({token.lower() for token in tokens})
				fout.write ("{0},{1}\n".format (js[UNIQ_KEY], uniqs))

def writeNTokens (key, srcfile, tgtfile, start=1827, end=1922):
	with open (srcfile) as fin, open (tgtfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			if js["year"] >= start and js["year"] <= end:
				tokens = js[key]
				fout.write ("{0},{1}\n".format (js[UNIQ_KEY], len(tokens)))

@plac.annotations(
	srcfile=("file containing the corpus", "positional"),
	statsdir=("directory containing all the statistics", "positional"),
	key=("key in the json file (also becomes the extension of the target file)", "positional"),
	prefix=("prefix for the file", "option"),
	start=("the start year", "option"),
	end=("the end year", "option")
)
def main (srcfile, statsdir, key, prefix="accessible", start=1827, end=1922):
	key_maps = {
		"filename": ("filename", writeIds),
		"newspaper": ("newspaper", writeNewspapers),
		"year": ("year", writeYear),
		"text": ("text", writeText),
		"tokens": ("tokens", writeTokens),
		"nuniqs": ("tokens", writeNUniqs),
		"ntokens": ("tokens", writeNTokens),
		"uncased": ("tokens", writeUncasedTokens)
	}

	tgtfile = os.path.join (statsdir, "{0}.{1}".format (prefix, key))
	fieldname, writeToFile = key_maps[key]
	writeToFile(fieldname, srcfile, tgtfile, start=start, end=end)

if __name__ == "__main__":
	plac.call (main)
