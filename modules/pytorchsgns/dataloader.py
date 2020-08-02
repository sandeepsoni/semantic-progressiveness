from collections import defaultdict

from .datastructures import Vocab

class RawReader (object):
	@classmethod
	def readDocs (cls, textFile, min_count=10, ws=10, subsampling=0.00001):
		def init_vocab (filename, min_count, subsampling):
			"""
			`filename` contains a document per line; tokens in a
			document are lowercased and separated by whitespace.   
			tokens with frequency less than `min_count` are discarded.
			TODO: downsample the higher frequency terms.
			TODO: implement max_vocab i.e restrict the vocab to a given size.
			"""
			w2i, i2w, counts = dict (), dict (), dict ()

			with open (textFile) as fin:
				for line in fin:
					tokens = line.strip().split(" ")
					for token in tokens:
						if token.isalpha():
							counts[token] = counts.get (token, 0) + 1

			discard = [key for key in counts if counts[key] < min_count]
			for key in discard:
				del counts[key]

			for key in counts:
				w2i[key] = len (w2i)
				i2w[w2i[key]] = key

			return w2i, i2w, counts

		def get_training_pairs (filename, w2i, i2w, ws):
			"""
			`filename` contains a document per line; tokens in a document are
			lowercased and separated by whitespace.
			`w2i` and `i2w` are indices that map words to numeric ids.
			ws is the size of the window -- only symmetric windows are supported.
			"""
			target_context_pairs = defaultdict (int)
			with open (filename) as fin:
				for doc_num, doc in enumerate (fin):
					tokens = doc.strip().split(" ")
					length = len (tokens)
					for i, token in enumerate (tokens):
						if token.isalpha() and token in w2i:
							for j in range (1, ws+1):
								if j < i and tokens[i-j] in w2i:
									target_context_pairs[(token, tokens[i-j])] += 1
								if 0 < j < (length-i) and tokens[i+j] in w2i:
									target_context_pairs[(token, tokens[i+j])] += 1
			
			return target_context_pairs

		w2i, i2w, counts = init_vocab (textFile, min_count, subsampling)
		target_context_pairs = get_training_pairs (textFile, w2i, i2w, ws)
		return Vocab (w2i, i2w, counts), target_context_pairs	
