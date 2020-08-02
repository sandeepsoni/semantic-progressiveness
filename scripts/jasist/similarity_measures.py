import numpy as np

def cosine_sim (v1: np.ndarray, v2: np.ndarray) -> float:
	""" Cosine similarity between two vectors."""
	return (np.dot (v1, v2)/(np.linalg.norm (v1, 2) * np.linalg.norm (v2, 2)))

def cosine_dist (v1: np.ndarray, v2:np.ndarray) -> float:
	""" Cosine distance between two vectors."""
	return 1 - cosine_sim(v1, v2)

def neighbors(word:str, embs:np.array, voc:tuple, k=3) -> list:
	""" Get the list of near neighbors for a given word from the embeddings.

		Each row of the matrix `embs` is a vector for a word.
		The mapping of words and row numbers is in `voc`.
	"""
	w2i, i2w = voc
	vec_len = np.linalg.norm (embs[w2i[word], :], 2)
	norms = np.linalg.norm (embs, 2, axis=1)

	sims = np.dot(embs[w2i[word],], embs.T)
	sims = sims / (vec_len * norms)

	output = []
	for sim_idx in sims.argsort()[::-1][1:(1+k)]:
		if sims[sim_idx] > 0:
			output.append(i2w[sim_idx])
	return output

def get_neighbor_sims(word:str, neighbors_set:set, vec: np.ndarray, voc:tuple) -> np.array:
	w2i, i2w = voc
	v_self = vec[w2i[word], :]
	v_neighbors = vec[[w2i[neighbor] for neighbor in neighbors_set], :]
	
	vec_len = np.linalg.norm (v_self, 2)
	norms = np.linalg.norm (v_neighbors, 2, axis=1)
	
	sims = np.dot (v_self, v_neighbors.T)
	sims = sims / (vec_len * norms)

	return sims

def hamilton_local_score (word:str, voc:tuple, old:np.array, new:np.array, k=50) -> float:
	near_neighbors_old = neighbors (word, old, voc, k=k)
	near_neighbors_new = neighbors (word, new, voc, k=k)
	common_neighbors = set (near_neighbors_old).union (near_neighbors_new)

	sim_old = get_neighbor_sims (word, common_neighbors, old, voc)
	sim_new = get_neighbor_sims (word, common_neighbors, new, voc)
	
	return cosine_dist (sim_old, sim_new)

def hamilton_global_score (word:str, voc:tuple, old:np.ndarray, new: np.ndarray) -> float:
	w2i, i2w = voc
	return cosine_dist (old[w2i[word],:], new[w2i[word], :])
