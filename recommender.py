import time, csv
import numpy as np

similarities = np.load('data/similarities.npy')
user_utility = np.load('data/user_utility_matrix.npy')
item_utility = np.load('data/item_utility_matrix.npy')

# assuming user_ids correspond to both utility matrix row
# indices as well as similarity matrix row indices

# takes as arguments a utility matrix (either item or user based)
# and the index of the element to predict on
# returns a vector of predicted ratings based on the N similar elements
def recommend(utility_matrix, element_id, N=10):
	# get similarities of that element to all other elements
	element_similarities = similarities[element_id]
	# sort the similarities
	sorted_element_sims = element_similarities.argsort()[::-1]
	# get indices of N most similar elements
	most_similar_indices = sorted_element_sims[:N]
	# get matrix with vectors of N most similar elements
	sim_vectors = utility_matrix[most_similar_indices, :]
	# collapse the matrix to get the generic similar element
	predicted_ratings = sim_vectors.mean(axis=0)
	# return the vector to do some testing
	return predicted_ratings

predict_vector = recommend(user_utility, 1)
highest_rating = predict_vector.argsort()[::-1][0]

print("Highest rating by generic similar user: ", predict_vector[highest_rating])
print("This corresponds to the show_id: ", highest_rating)
