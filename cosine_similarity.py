import numpy as np
import time

# import the utility matrix computed before:
matrix = np.load('utility_matrix.npy')
print("we here")
print(matrix.shape)
'''

# this calculates the similarity of each row with each row,
# resulting in a matrix of shape (num_users, num_users) where
# each row contains the similarity between the user that
# corresponds to that row and every other user (there will always
# be one element of that row with the value 1 because that is
# the similarity between that user and itself)
results = []
rows_in_slice = 100

slice_start = 0
slice_end = slice_start + rows_in_slice

while slice_end <= matrix.shape[0]:

    results.append(matrix[slice_start:slice_end].dot(matrix.T).max(axis=1))

    slice_start += rows_in_slice
    slice_end = slice_start + rows_in_slice

result = np.concatenate(results)

print("Finished computing similarities... (after {})".format(time.time()-t0))
cos_sims = cosine(matrix)
np.save('similarities', cos_sims)
'''
