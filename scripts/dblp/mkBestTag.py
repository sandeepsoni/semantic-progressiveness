import plac
import glob
import os

def bestTag (dist):
	return max (dist.items(), key=lambda x:x[1])[0]

def get_dist (line):
	parts = line.split()
	d = {part.split(":")[0]:float(part.split(":")[-1]) for part in parts[1:]}
	return parts[0], d

@plac.annotations(
	probfile=("The file with output of P(tag) for every word", "positional"),
	tagfile=("The file with the best tag for every word", "positional")
)
def main (probfile, tagfile):
	complete_dist = dict ()
	with open (probfile) as fin:
		for line in fin:
			line = line.strip()
			if len (line) > 0:
				word, dist = get_dist(line.strip())
				if word not in complete_dist:
					complete_dist[word] = dict ()
				complete_dist[word] = dist

	best_tags = dict ()
	for w in complete_dist:
		best_tags[w] = bestTag (complete_dist[w])
	
	with open (tagfile, "w") as fout:
		for w in best_tags:
			fout.write ("{0}\t{1}\n".format (w, best_tags[w]))
	
if __name__ == "__main__":
	plac.call (main)
