import plac
import os
import pandas as pd

def df2dict (df, key, val):
	keys = df[key].values
	vals = df[val].values

	assert (len(keys) == len (vals))
	return {keys[i]: vals[i] for i in range (len(keys))}

def readCaseFile (filename, key, value):
	df = pd.read_csv (filename, sep=",", header=None, names=["word", "lower_ratio", "upper_ratio", "title_ratio", "count"])
	df["lower_ratio"] = df["lower_ratio"] / df["count"]
	df["upper_ratio"] = df["upper_ratio"] / df["count"]
	df["title_ratio"] = df["title_ratio"] / df["count"]
	words_asdict = df2dict (df, key, value)
	return words_asdict

def readWordScores (filename, sep=","):
	words = dict ()
	with open (filename) as fin:
		for line in fin:
			parts = line.strip().split(sep)
			words[parts[0]] = float (parts[1])
	return words

def readNames (filename):
	names = set ()
	with open (filename) as fin:
		for line in fin:
			parts = line.strip().split("\t")
			if len (parts) == 2:
				if parts[1] == "NNP" or parts[1] == "NNPS":
					names.add (parts[0])
	return names

REMOVE_LIST = {"ofa", "witha", "ona", "anda", "asthe", "andthe", "tothe", "ditional", "lated"}

def isPresent (word, E, L):
	return word in E["count"] and word in L["count"]

def isMoreThanCount (word, E, L, count_thresh=10):
	return isPresent (word, E, L) and (E["count"][word] >= count_thresh and L["count"][word] >= count_thresh)

def isRareRisingWord (word, E, L, count_thresh=10, ratio_thresh=5): 
	return isPresent (word, E, L) and E["count"][word] < count_thresh and L["count"][word] >= count_thresh and(L["count"][word] / E["count"][word]) >= ratio_thresh

def isAbbrev (word, E, L, upper_thresh=0.25, title_thresh=0.9):
	return isPresent (word, E, L) and (E["upper"][word] >= upper_thresh or L["upper"][word] >= upper_thresh or E["title"][word] >= title_thresh or L["title"][word] >= title_thresh)

def isNotAbbrev (word, E, L, upper_thresh=0.25, title_thresh=0.9):
	return not isAbbrev (word, E, L, upper_thresh, title_thresh)

def isAcceptableAbbrev (word, E, L, upper_thresh=0.25, title_thresh=0.9, count_thresh=100): 
	return isAbbrev (word, E, L, upper_thresh=upper_thresh, title_thresh=title_thresh) and ((E["count"][word] >= count_thresh) or (L["count"][word] >= count_thresh))

def isNonName (word, E, L, names):
	return isPresent (word, E, L) and (word not in names)

def isNotInRemoveList (word):
	global REMOVE_LIST

	return word not in REMOVE_LIST

def readCaseStats (filename):
	cases = dict ()
	cases["lower"] = readCaseFile (filename, "word", "lower_ratio")
	cases["upper"] = readCaseFile (filename, "word", "upper_ratio")
	cases["title"] = readCaseFile (filename, "word", "title_ratio")
	cases["count"] = readCaseFile (filename, "word", "count")
	return cases

@plac.annotations (
	dirname=("directory with all the files", "positional"),
	earlyfile=("case stats file for early model", "positional"),
	laterfile=("case stats file for later model", "positional"),
	besttagfile=("best tag file", "positional"),
	changelistfile = ("change list file", "positional"),
	tgtfile=("target file", "positional")
)
def main (dirname, earlyfile, laterfile, besttagfile, changelistfile, tgtfile):
	CNT_THRESH1 = 10
	CNT_THRESH2 = 250
	RATIO_THRESH= 10
	UPPER_THRESH= 0
	TITLE_THRESH=0.25

	earlyfile = os.path.join (dirname, earlyfile)
	early = readCaseStats (earlyfile)

	laterfile = os.path.join (dirname, laterfile)
	later = readCaseStats (laterfile)

	changelistfile = os.path.join (dirname, changelistfile)
	vocab = readWordScores (changelistfile, sep="\t")
	top_words = list (map(lambda x:x[0], sorted (vocab.items(), key=lambda x:x[1], reverse=True)))
	names = readNames (os.path.join (dirname, besttagfile))

	keepmask_presence = list()
	keepmask_count = list ()
	keepmask_rare = list ()
	keepmask_isnotabbrev = list ()
	keepmask_isacceptableabbrev = list ()
	keepmask_names = list ()
	keepmask_hardremove = list ()

	for word in top_words:
		keepmask_presence.append (isPresent (word, early, later))
		keepmask_count.append (isMoreThanCount(word, early, later, count_thresh=CNT_THRESH1))
		keepmask_rare.append (isRareRisingWord(word, early, later, count_thresh=CNT_THRESH1, ratio_thresh=RATIO_THRESH))
		keepmask_isnotabbrev.append (isNotAbbrev(word, early, later, upper_thresh=UPPER_THRESH, title_thresh=TITLE_THRESH))
		keepmask_isacceptableabbrev.append (isAcceptableAbbrev (word, early, later, upper_thresh=UPPER_THRESH, title_thresh=TITLE_THRESH, count_thresh=CNT_THRESH2))
		keepmask_names.append (isNonName(word, early, later, names))
		keepmask_hardremove.append (isNotInRemoveList (word))

	keep = list ()
	discarded = list ()
	for i, word in enumerate (top_words):#(top_words[0:int(len(top_words)/2)]):
		keep_based_on_frequency = keepmask_presence[i] and (keepmask_count[i] or keepmask_rare[i])
		keep_based_on_abbrevs = keepmask_isnotabbrev[i] or keepmask_isacceptableabbrev[i]
		if not keep_based_on_frequency or not keep_based_on_abbrevs or not keepmask_hardremove[i]: #or not keepmask_names[i] :
			discarded.append (word)
		else:
			keep.append (word)        

	print ("Kept words: {0}, Discarded words: {1}, Total: {2}".format (len(keep), len(discarded), len (keep) + len (discarded)))

	with open (os.path.join (dirname, tgtfile), "w") as fout:
		for word in keep[0:1000]:
			fout.write ("{}\n".format (word))
	
	print ("Written the top 1000 words to file")

if __name__ == "__main__":
	plac.call (main)
