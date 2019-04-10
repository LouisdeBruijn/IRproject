from sklearn.metrics.pairwise import cosine_similarity as cosine
import numpy as np
import time

# constants
t0 = time.time()
method = "user_based"
slice_size = 100

# import the utility matrix computed before:
if method == "user_based":
    matrix = np.load('user_utility_matrix.npy')
elif method == "item_based":
    matrix = np.load('item_utility_matrix.npy')
elif method == "TESTING":
    matrix = np.random.rand(10, 10)

print(f"Finished loading the matrix... (after {time.time()-t0})")

# the whole thing does not fit into memory, so we do it row by row
slice_start = 0
slice_end = slice_start + slice_size

slice2_start = 0
slice2_end = slice2_start + slice_size

final_cos = list()

# TODO: Compute this differently / more efficiently

# TODO: OR figure out how the indices between matrix rows and
# cos_sims rows relate

# while we have not reached the last row
while slice_end <= matrix.shape[0]:
    cos_sims = list()
    while slice2_end <= matrix.shape[0]:
        # take the next slice_size rows, and compute the cosine similarity
        # between those rows and the entire matrix
        cos_sims.append(cosine(matrix[slice_start:slice_end], matrix[slice2_start:slice2_end]))
        #print("length of cos sims: ", len(cos_sims))
        #print("shape: ", cos_sims[0].shape)
        # increment the slice start and end
        slice2_start += slice_size
        slice2_end = slice2_start + slice_size
    # increment the slice start and end
    slice2_start = 0
    slice2_end = slice2_start + slice_size
    # concatenate list into one long row
    final_cos.append(np.concatenate(cos_sims, axis=1))
    print("length of final cos: ",len(final_cos))
    # reset inner loop iterators
    slice_start += slice_size
    slice_end = slice_start + slice_size

# convert back into a numpy array (appending is faster than concatenating)
cos_sims = np.concatenate(final_cos)

print("Finished computing similarities... (after {})".format(time.time()-t0))
print("Cosine similarity matrix shape: ", cos_sims.shape)

if method != "TESTING":
    np.save('similarities', cos_sims)
