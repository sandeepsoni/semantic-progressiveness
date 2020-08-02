import plac
import glob
import os

def tag_prob (dist, tag):
	probs = dict ()
	for w in dist:
		if tag not in dist[w]:
			probs[w] = 0
		else:
			probs[w] = dist[w][tag]/sum(dist[w].values())

	return probs

def get_dist (line):
	parts = line.split()
	d = {part.split(":")[0]:int(part.split(":")[-1]) for part in parts[1:]}
	return parts[0], d

def merge_dist (d1, d2):
	merged = dict ()
	keys = list (set(list (d1.keys())) | set (list (d2.keys())))

	for key in keys:
		if key in d1 and key in d2:
			merged[key] = d1[key] + d2[key]
		elif key in d1:
			merged[key] = d1[key]
		elif key in d2:
			merged[key] = d2[key]

	return merged

@plac.annotations(
	filepattern=("The pattern of the filenames containing PoS statistics", "positional"),
	probfile=("The file with output of P(tag) for every word", "positional")
)
def main (filepattern, probfile):
	filepattern = filepattern.replace ("+","*")
	complete_dist = dict ()
	for filename in glob.glob (filepattern):
		with open (filename) as fin:
			for line in fin:
				line = line.strip()
				if len (line) > 0:
					word, dist = get_dist(line.strip())
					if word.isalpha():
						if word not in complete_dist:
							complete_dist[word] = dict ()
						complete_dist[word] = merge_dist (complete_dist[word], dist)
	
	with open (probfile, "w") as fout:
		for w in complete_dist:
			fout.write ("{0}".format (w))
			z = sum(list (complete_dist[w].values()))
			for tag in complete_dist[w]:
				fout.write ("\t")
				fout.write ("{0}:{1:.4f}".format (tag, complete_dist[w][tag]/z))
			fout.write ("\n")
	
if __name__ == "__main__":
	plac.call (main)
