import gensim
import numpy as np

def intersection_align_gensim(m1,m2, words=None):
	""" Intersect two gensim word2vec models, m1 and m2, and keep only the shared vocabulary.
		Original code from https://gist.github.com/quadrismegistus/09a93e219a6ffc4f216fb85235535faf

		Modified code to support the current version of gensim
		
		The basic idea is to first obtain a vocabulary common to both the models; 
		then sort the vocabulary by frequency; then update the internal indices and vocabularies of
		gensim models.
		
		Parameters
		----------

		:m1,m2: gensim.models.Word2Vec
			The two gensim models that hold the word embeddings
		:words: set or None
			if `words` is a set, then the overall vocabulary is the intersection with this set also.

		
		TODO: Check if the alignment remains valid when applied sequentially.
		TODO: Assuming `words` is a subset of vocabulary and a list, always maintain the same order
			  internally as the supplied list
    """

	# Get the vocab for each model
	vocab_m1 = set(m1.wv.vocab.keys())
	vocab_m2 = set(m2.wv.vocab.keys())

	# Find the common vocabulary
	common_vocab = vocab_m1&vocab_m2
	if words: common_vocab&=set(words)

	# Otherwise sort by frequency (summed for both)
	common_vocab = list(common_vocab)
	common_vocab.sort(key=lambda w: m1.wv.vocab[w].count + m2.wv.vocab[w].count,reverse=True)

	# Then for each model...
	for m in [m1,m2]:
		# Replace old syn0norm array with new one (with common vocab)
		indices = [m.wv.vocab[w].index for w in common_vocab]
		old_arr = m.wv.vectors_norm
		m.wv.vectors_norm = m.wv.vectors = old_arr[indices, :]

		# Replace old syn1neg array with new one (with common vocab)
		# Strictly speaking, this is not needed.
		old_contexts = m.trainables.syn1neg
		m.trainables.syn1neg = old_contexts[indices, :]

		# Replace old vocab dictionary with new one (with common vocab)
		# and old index2word with new one
		m.wv.index2word = common_vocab
		old_vocab = m.wv.vocab
		new_vocab = {}
		for new_index,word in enumerate(common_vocab):
			old_vocab_obj=old_vocab[word]
			new_vocab[word] = gensim.models.word2vec.Vocab(index=new_index, count=old_vocab_obj.count)
		m.wv.vocab = new_vocab

	return (m1,m2)

def smart_procrustes_align_gensim(base_embed, other_embed, words=None):
	""" Procrustes align two gensim word2vec models (to allow for comparison between same word across models).
		Original code from https://gist.github.com/quadrismegistus/09a93e219a6ffc4f216fb85235535faf

		Modified code to support the current version of gensim (by Sandeep)

		The basic idea is to first intersect and align the indices of the vocabularies of each model; then
		applying the procrustes orthogonal aligment method using SVD; then replacing the internal vectors
		that represent the embeddings for the alignmed model with the solution.

		Parameters
		----------

		:base_embed: gensim.models.Word2Vec
			The base embedding model i.e the one *onto* which we align.

		:other_embed: gensim.models.Word2Vec
			The other embedding model i.e the model which needs to be aligned.

		:words: set or None
			If `words` is set, intersect the common vocabulary further with the given set

	"""

	base_embed.init_sims()
	other_embed.init_sims()

	# make sure vocabulary and indices are aligned
	in_base_embed, in_other_embed = intersection_align_gensim(base_embed, other_embed, words=words)

	# get the embedding matrices
	base_vecs = in_base_embed.wv.vectors_norm
	other_vecs = in_other_embed.wv.vectors_norm

	# procrustes alignment solution
	M = other_vecs.T.dot(base_vecs) 
	U, _, V = np.linalg.svd(M)
	R = U.dot(V) 
	
	# Replace original array with modified one
	# i.e. multiplying the embedding matrix (vectors_norm)by "R"
	other_embed.wv.vectors_norm = other_embed.wv.vectors = (other_embed.wv.vectors_norm).dot(R)
	return other_embed
