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
with open('rating.csv') as csv_file:
    ratings = csv.reader(csv_file, delimiter=',')
    for idx, row in enumerate(ratings):
        user_id, anime_id, rating = row
        matrix[user_id][anime_id] = rating

print(f"Finished reading the data... (after {t0-time.time()})")

# checks if the value is a valid rating
def is_rating(value):
    return not value == -1

# normalize ratings for each row in utility matrix
for row_idx in range(num_users):
    # only valid ratings should be used to calculate avg_rating
    ratings = filter(is_rating, matrix[row_idx])
    avg_rating = sum(ratings) / len(ratings)
    # for each element in the matrix row, subtract the average
    # rating. if it is not a valid rating, set the value to 0
    for col_idx in range(num_shows):
        if is_rating(matrix[row_idx][col_idx]):
            matrix[row_idx][col_idx] -= avg_rating
        else:
            matrix[row_idx][col_idx] == 0

print(f"Finished normalizing the data... (after {t0-time.time()})")

# this calculates the similarity of each row with each row,
# resulting in a matrix of shape (num_users, num_users) where
# each row contains the similarity between the user that
# corresponds to that row and every other user (there will always
# be one element of that row with the value 1 because that is
# the similarity between that user and itself)
cos_sims = cosine(matrix)

print(f"Finished computing similarities... (after {t0-time.time()})")

np.save('utility_matrix', matrix)
np.save('similarities', cos_sims)
