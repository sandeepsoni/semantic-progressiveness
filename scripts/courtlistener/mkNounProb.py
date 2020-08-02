import plac
import glob
import os

def nounProb (dist):
	prob = 0
	if "NNP" in dist and "NNPS" in dist:
		prob = dist["NNP"] + dist["NNPS"]
	elif "NNP" in dist:
		prob = dist["NNP"]
	elif "NNPS" in dist:
		prob = dist["NNPS"]
	
	return prob

def get_dist (line):
	parts = line.split()
	d = {part.split(":")[0]:float(part.split(":")[-1]) for part in parts[1:]}
	return parts[0], d

@plac.annotations(
	probfile=("The file with output of P(tag) for every word", "positional"),
	nounfile=("The file with the proper noun probability for every word", "positional")
)
def main (probfile, nounfile):
	complete_dist = dict ()
	with open (probfile) as fin:
		for line in fin:
			line = line.strip()
			if len (line) > 0:
				word, dist = get_dist(line.strip())
				if word not in complete_dist:
					complete_dist[word] = dict ()
				complete_dist[word] = dist

	noun_probs = {w: nounProb (complete_dist[w]) for w in complete_dist}
	
	with open (nounfile, "w") as fout:
		for w in noun_probs:
			fout.write ("{0}\t{1}\n".format (w, noun_probs[w]))
	
if __name__ == "__main__":
	plac.call (main)
