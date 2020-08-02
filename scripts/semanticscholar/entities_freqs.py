import ujson
import plac
from collections import defaultdict
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
MILLION = 1000000

@plac.annotations(
	srcfile=("the source filename", "positional"),
	tgtfile=("the target filename", "positional")
)
def main (srcfile, tgtfile):
	entities_token_freqs = defaultdict (int)
	entities_doc_freqs = defaultdict (int)

	with open (srcfile) as fin:
		for i, line in enumerate (fin):
			js = ujson.loads (line) 
			entities = js["entities"]
			for entity in entities:
				words = entity.split()
				for word in words:
					entities_token_freqs[word.lower()] += 1
				for word in set (words):
					entities_doc_freqs[word.lower()] += 1
			if (i+1) % MILLION == 0:
				logging.info ("Processed {0} lines".format (i+1))

	with open (tgtfile, "w") as fout:
		for w in entities_token_freqs:
			fout.write ("{0},{1},{2}\n".format (w, entities_token_freqs[w], entities_doc_freqs[w]))

	
if __name__ == "__main__":
	plac.call(main)
