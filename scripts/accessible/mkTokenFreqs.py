import ujson
import plac
from collections import defaultdict

@plac.annotations(
	corpusfile=("corpus file (json per line)", "positional"),
	tokensfile=("the tokens file", "positional")
)
def main (corpusfile, tokensfile):
	V = defaultdict (int)
	D = defaultdict (int)
	with open (corpusfile) as fin, open (tokensfile, "w") as fout:
		for line in fin:
			js = ujson.loads (line)
			tokens = list (map(lambda x:x.lower(), js["tokens"]))
			for token in tokens:
				V[token] += 1
			for token in set (tokens):
				D[token] += 1

		for key in sorted (V):
			fout.write ("{0}\t{1}\t{2}\n".format (key, V[key], D[key]))
	
if __name__ == "__main__":
	plac.call (main)
