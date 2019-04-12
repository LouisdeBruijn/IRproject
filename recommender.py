import time, csv
import numpy as np
import math

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
	# item and user matricies have swapped dimensions
	if utility_matrix.shape[0] > utility_matrix.shape[1]:
		# get matrix with vectors of N most similar elements
		sim_vectors = utility_matrix[most_similar_indices, :]
		# collapse the matrix to get the generic similar element
		predicted_ratings = sim_vectors.mean(axis=0)
	else:
		# get matrix with vectors of N most similar elements
		sim_vectors = utility_matrix[:, most_similar_indices]
		# collapse the matrix to get the generic similar element
		predicted_ratings = sim_vectors.mean(axis=1)
	# return the vector to do some testing
	return predicted_ratings

# returns the root mean square error (RMSE) between two vectors
def RMSE(vector1, vector2):
	return math.sqrt(np.square(vector1 - vector2).mean())

# run num_tests tests and return the MSE error values
def test(utility_matrix, num_tests=None):
	errors = list()
	# if we dont provide a number of tests, test all rows
	if num_tests is None:
		num_tests = utility_matrix.shape[0]
	for test_id in range(num_tests):
		# get the predicted vector
		predict_vector = recommend(utility_matrix, test_id)
		# item and user matrices have swapped dimensions
		if utility_matrix.shape[0] > utility_matrix.shape[1]:
			# get the target vector
			target_vector = utility_matrix[test_id]
		else:
			# get the target vector
			target_vector = utility_matrix[:, test_id]
		# compute MSE
		errors.append(MSE(predict_vector, target_vector))
	return errors

user_errors = test(user_utility)
item_errors = test(item_utility)

print("Total MSE for user_based: ", sum(user_errors))
print("Total MSE for item_based: ", sum(item_errors))



#highest_rating = predict_vector.argsort()[::-1][0]
#print("Highest rating by generic similar user: ", predict_vector[highest_rating])
#print("This corresponds to the show_id: ", highest_rating)

