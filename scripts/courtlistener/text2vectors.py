import gensim, logging, os, plac, ujson
import numpy as np
from gensim.models.callbacks import CallbackAny2Vec

import sys
if "../../" not in sys.path:
	sys.path.append ("../../")

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class Sents (object):
	def __init__ (self, filename):
		self.filename = filename

	def __iter__ (self):
		with open (self.filename) as fin:
			for line in fin:
				tokens = [token for token in line.strip().split() if token.isalpha()]
				yield tokens

@plac.annotations (
	src=("the source file that contains text", "positional"),
	tgt=("the target file with the model", "positional"),
	seed=("the seed value to initialize the model", "option", None, int)
)
def main (src, tgt, seed=42):
	sents = Sents (src)
	model = gensim.models.Word2Vec (sents,
									min_count=10,
									size=300, 
									sg=1, 
									negative=15, 
									compute_loss=True, 
									workers=8, 
									ns_exponent=0.75, 
									window=10, 
									iter=15,
									seed=seed)
	model.save (tgt)

if __name__ == "__main__":
	plac.call (main)
