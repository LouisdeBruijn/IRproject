from sklearn.metrics.pairwise import cosine_similarity as cosine
from sklearn.preprocessing import normalize
import numpy as np
import time

# constants
t0 = time.time()
method = "user_based"

# import the utility matrix computed before:
if method == "user_based":
    matrix = np.load('data/user_utility_matrix.npy')
elif method == "item_based":
    matrix = np.load('data/item_utility_matrix.npy')
elif method == "TESTING":
    matrix = np.random.rand(10, 10)

print(f"Finished loading the matrix... (after {time.time()-t0})")

# dot product between unit-normalized vectors is equivalent to cosine similarity
# this is according to a SO answer, but when comparing it to the cosine function
# on a smaller matrix it appears to be correct.
# run this script with method = "TESTING" to see for yourself
normalized_matrix = normalize(matrix, axis=1)
cos_sims = np.dot(normalized_matrix, normalized_matrix.T)

if method == "TESTING":
    with np.printoptions(precision=3):
        print(cosine(matrix))
        print("")
        print(cos_sims)

print("Finished computing similarities... (after {})".format(time.time()-t0))
print("Cosine similarity matrix shape: ", cos_sims.shape)

if method != "TESTING":
    np.save('data/similarities', cos_sims)
