from sklearn.metrics.pairwise import cosine_similarity as cosine
import numpy as np
import csv, time

# constants
t0 = time.time()
num_users = 73516
num_shows = 12294

# initialize utility matrix with -1 as default value
matrix = np.full((num_users, num_shows), -1, dtype=int)

# read data, and fill in the utiliy matrix
# watched but not rated is treated the same as not watched
with open('data/rating.csv') as csv_file:
    ratings = csv.reader(csv_file, delimiter=',')
    next(ratings, None) # skip the header
    # anime show ids dont correspond to idx numbers, they are unique
    # id numbers from the website itself, so we have to map them to 
    # indices with a dictionary. To find the anime_id of col_idx, do
    # anime_id = anime_id_mappings[col_idx]
    anime_id_mappings = dict()
    show_number = 0
    for idx, row in enumerate(ratings):
        user_id, anime_id, rating = map(int, row)
        if anime_id in anime_id_mappings:
            anime_id = anime_id_mappings[anime_id]
        else:
            anime_id_mappings[anime_id] = show_number
            anime_id = show_number
            show_number += 1
        matrix[user_id - 1][anime_id - 1] = rating

print("Finished reading the data... (after {})".format(time.time()-t0))

# checks if the value is a valid rating
def is_rating(value):
    return not value == -1

# normalize ratings for each row in utility matrix
num_users_with_no_ratings = 0
for row_idx in range(num_users):
    # only valid ratings should be used to calculate avg_rating
    ratings = list(filter(is_rating, matrix[row_idx]))
    if len(ratings) > 0:
        avg_rating = sum(ratings) / len(ratings)
        # for each element in the matrix row, subtract the average
        # rating. if it is not a valid rating, set the value to 0
        for col_idx in range(num_shows):
            if is_rating(matrix[row_idx][col_idx]):
                matrix[row_idx][col_idx] -= avg_rating
            else:
                matrix[row_idx][col_idx] == 0
    else:
        num_users_with_no_ratings += 1
print("Number of users who did not rate anything: {}".format(num_users_with_no_ratings))

print("Finished normalizing the data... (after {})".format(time.time()-t0))


# the whole thing does not fit into memory, so we do 100 rows at a time
cos_sims = list()
slice_size = 100
slice_start = 0
slice_end = slice_start + slice_size

# while we have not reached the last row
while slice_end <= matrix.shape[0]:
    # take the next slice_size rows, and compute the cosine similarity
    # between those rows and the entire matrix
    cos_sims.append(cosine(matrix[slice_start:slice_end], matrix))
    # increment the slice start and end
    slice_start += slice_size
    slice_end = slice_start + slice_size

# convert back into a numpy array (appending is faster than concatenating)
cos_sims = np.concatenate(cos_sims)

# we end up with a numpy matrix of size (num_users, num_users) where each row
# contains the results of the cosine similarity between that user and each other
# user (it will always contain the value 1 for the cosine similarity between it
# and itself)

# example:
# m == matrix of size (5, 2)
# c == cosine(m) == matrix of size (5, 5)
# c[0] == similarities between m[0] and m[:]

print(f"Finished computing similarities... (after {time.time()-t0})")

np.save('utility_matrix', matrix)
np.save('similarities', cos_sims)

print(f"Finished saving the results to file... (after {time.time()-t0})")