import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as cosine
import time

# import the utility matrix computed before:
matrix = np.load('utility_matrix.npy')
print("we here")
t0 = time.time()
# the whole thing does not fit into memory, so we do 100 rows at a time


slice_size = 100
slice_start = 0
slice_end = slice_start + slice_size

slice2_size = 100
slice2_start = 0
slice2_end = slice2_start + slice2_size

final_cos = list()

# while we have not reached the last row
while slice_end <= matrix.shape[0]:
    cos_sims = list()
    while slice2_end <= matrix.shape[0]:
        # take the next slice_size rows, and compute the cosine similarity
        # between those rows and the entire matrix
        cos_sims.append(cosine(matrix[slice_start:slice_end], matrix[slice2_start:slice2_end]))
        print("length of cos sims: ", len(cos_sims))
        print("shape: ", cos_sims[0].shape)
        # increment the slice start and end
        slice2_start += slice2_size
        slice2_end = slice2_start + slice2_size
        #print("Time to compute one batch..... ({})".format(time.time()-t0))
    slice2_size = 100
    slice2_start = 0
    slice2_end = slice2_start + slice2_size    
    final_cos.append(np.concatenate(cos_sims, axis=1))
    print("length of final cos: ",len(final_cos))
    slice_start += slice_size
    slice_end = slice_start + slice_size

# convert back into a numpy array (appending is faster than concatenating)
cos_sims = np.concatenate(final_cos)


print("Finished computing similarities... (after {})".format(time.time()-t0))
np.save('similarities', cos_sims)
print(cos_sims.shape)
