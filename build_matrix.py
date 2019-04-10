from sklearn.metrics.pairwise import cosine_similarity as cosine
import numpy as np
import csv, time

# constants
t0 = time.time()
num_users = 7914
num_shows = 2746
path_to_data = 'ratings_250.csv'
#using_subset = True
method = "item_based"

# using the subset of the data
if method == "using_subset":
    num_users = 15
    path_to_data = 'ratings_250.csv'

# switch these variables based on the method so that we can 
# re-use the same algorithm to calculate similarities.
if method == "user_based":
    matrix_dimensions = (num_users, num_shows)
    num_rows = num_users
    num_cols = num_shows
elif method == "item_based":
    matrix_dimensions = (num_shows, num_users)
    num_rows = num_shows
    num_cols = num_users

# initialize utility matrix with -1 as default value
matrix = np.full(matrix_dimensions, -1, dtype=int)

# read data, and fill in the utiliy matrix
# watched but not rated is treated the same as not watched
with open(path_to_data) as csv_file:
    ratings = csv.reader(csv_file, delimiter=',')
    #next(ratings, None) # skip the header
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
        if method == "user_based":
            (row_idx, col_idx) = (user_id - 1, anime_id - 1)
        elif method == "item_based":
            (row_idx, col_idx) = (anime_id - 1, user_id - 1)
        matrix[row_idx][col_idx] = rating

print("Finished reading the data... (after {})".format(time.time()-t0))

# checks if the value is a valid rating
def is_rating(value):
    if value == -1:
        return False

# normalize ratings for each row in utility matrix
num_users_with_no_ratings = 0
for row_idx in range(num_rows):
    # only valid ratings should be used to calculate avg_rating
    ratings = list(filter(is_rating, matrix[row_idx]))
    if len(ratings) > 0:
        avg_rating = sum(ratings) / len(ratings)
        # for each element in the matrix row, subtract the average
        # rating. if it is not a valid rating, set the value to 0
        for col_idx in range(num_cols):
            if is_rating(matrix[row_idx][col_idx]):
                matrix[row_idx][col_idx] -= avg_rating
            else:
                matrix[row_idx][col_idx] = 0
    else:
        num_users_with_no_ratings += 1

print("Number of users/shows who did not rate anything / did not get rated: {}".format(num_users_with_no_ratings))

print("Finished normalizing the data... (after {})".format(time.time()-t0))

if method == "user_based":
    np.save('user_utility_matrix', matrix)
elif method == "item_based":
    np.save('item_utility_matrix', matrix)

print("Finished saving the results to file... (after {})".format(time.time()-t0))
