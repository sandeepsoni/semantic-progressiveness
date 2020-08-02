import plac
import os

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
			names.add (line.strip())
	return names

@plac.annotations (
	dirname=("directory with all the files", "positional"),
	innovationsfile=("innovations file", "positional"),
	neuralnamesfile=("neural names file", "positional"),
	taggingnamesfile=("tagging names file", "positional"),
	oldlistfile=("tagging names file", "positional"),
	tgtfile=("target file", "positional")
)
def main (dirname, innovationsfile, neuralnamesfile, taggingnamesfile, oldlistfile, tgtfile):
	neuralnames = readNames (os.path.join (dirname, neuralnamesfile))
	taggingnames = readNames (os.path.join (dirname, taggingnamesfile))

	all_names = neuralnames | taggingnames
	

	vocab = readWordScores (os.path.join (dirname, innovationsfile), sep="\t")
	top_words = list (map(lambda x:x[0], sorted (vocab.items(), key=lambda x:x[1], reverse=True)))

	innovations = [top_word for top_word in top_words if top_word not in all_names and not len (top_word) < 3]
	old_list = readNames (os.path.join (dirname, oldlistfile))
	print ("Kept {}/{} words".format (len (innovations), len (top_words)))
	with open (os.path.join (dirname, tgtfile), "w") as fout:
		for word in innovations[2000:4000]:
			fout.write ("{}, {}\n".format (word, word in old_list))

	print ("Written the top 5000 words to file")

if __name__ == "__main__":
	plac.call (main)
