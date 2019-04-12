import time, csv
import numpy as np
import math

t0 = time.time()

user_sims = np.load('data/user_similarities.npy')
item_sims = np.load('data/item_similarities.npy')
user_util = np.load('data/user_utility_matrix.npy')
item_util = np.load('data/item_utility_matrix.npy')

print(f"Finished loading the matrices and similarities... (after {time.time()-t0})")

# assuming user_ids correspond to both utility matrix row
# indices as well as similarity matrix row indices

# takes as arguments a utility matrix (either item or user based)
# and the index of the element to predict on
# returns a vector of predicted ratings based on the N similar elements
def recommend(utility_matrix, element_id, N=10):
	# there are more users than shows, if there are more rows than cols
	# then that means we built that matrix with user_based method
	if utility_matrix.shape[0] > utility_matrix.shape[1]:
		method = "user_based"
	else:
		method = "item_based"

	# get similarities of that element to all other elements
	if method == "user_based":
		element_similarities = user_sims[element_id]
	else:
		element_similarities = item_sims[element_id]
	# sort the similarities
	sorted_element_sims = element_similarities.argsort()[::-1]
	# get indices of N most similar elements
	# skip the highest similarity (of the element to itself == 1)
	most_similar_indices = sorted_element_sims[1:N+1]

	if method == "user_based":
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


# returns the mean square error (MSE) between two vectors
def MSE(vector1, vector2):
	return np.square(vector1 - vector2).mean()


# run num_tests tests and return the RMSE error values
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
		# compute RMSE
		errors.append(MSE(predict_vector, target_vector))
		
	return errors


user_errors = test(user_utility)
item_errors = test(item_utility)
RMSE_user = math.sqrt(sum(user_errors))
RMSE_item = math.sqrt(sum(item_errors))
RMSE_average_user = math.sqrt(sum(user_errors))/len(user_utility)
RMSE_average_item = math.sqrt(sum(item_errors))/len(item_utility)

print(MSE(np.array([5, 3]), np.array([4.8, 2.6])))

print("Total RMSE for user_based: ", RMSE_user)
print("Total RMSE for item_based: ", RMSE_item)
print("Total MSE for user_based: ", sum(user_errors))
print("Total MSE for item_based: ", sum(item_errors))
print("Percentage of MSE over the user_based data: ", round((100/len(user_utility)*sum(user_errors)),2), "%")
print("Percentage of MSE over the item_based data: ", round((100/len(item_utility)*sum(item_errors)),2), "%")

print(f"Finished predicting and testing... (after {time.time()-t0})")
