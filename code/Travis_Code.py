import time
import csv
import numpy as np
from operator import itemgetter

# TODO: hide lockbox data and split train/test data
# TODO: adapt this to work with new data set

class Recommender:
    def __init__(self, verbose=True, parse_user_sims=True, parse_VIP_sims=True):
        self.start_time = time.time()
        self.user_count = 0
        self.VIP_count = 0
        # The sets contain the usernames
        self.VIPs = set()
        self.users = set()
        # These dicts contain the usernames as keys, and indices as values
        self.VIP_indices = dict()
        self.user_indices = dict()
        # These dicts contain the indices as keys, and usernames as values
        self.VIP_names = dict()
        self.user_names = dict()
        # The utility matrix contains booleans for whether user follows VIP
        self.matrix = np.zeros((5809, 2014), bool)
        # This will contain the column sums of the utility matrix
        # In other words: How many followers a VIP has based on our data
        self.VIP_pops = None
        # These store the similarities with (k, v) = (username, list(similarities))
        self.similar_users = dict()
        self.similar_VIPs = dict()
        # This holds variables i want to check out for debugging
        self.vars = dict()

        self.read_training_data()
        if verbose:
            timer = time.time() - self.start_time
            print(f"-> Read training data after {timer}\n")

        if parse_user_sims:
            self.get_user_similarities()
            if verbose:
                timer = time.time() - self.start_time
                print(f"-> Read user similarities after {timer}\n")

        if parse_VIP_sims:
            self.get_VIP_similarities()
            if verbose:
                timer = time.time() - self.start_time
                print(f"-> Read VIP similarities after {timer}\n")

    '''
    Read the training data, build utility matrix and fill variables.
    '''
    def read_training_data(self):
        with open('Twitter2014/matrix_training.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            for row in csv_reader:
                if row[0] not in self.users:
                    self.user_indices[row[0]] = self.user_count
                    self.user_names[self.user_count] = row[0]
                    self.user_count += 1
                    self.users.add(row[0])
                if row[1] not in self.VIPs:
                    self.VIP_indices[row[1]] = self.VIP_count
                    self.VIP_names[self.VIP_count] = row[1]
                    self.VIP_count += 1
                    self.VIPs.add(row[1])
                row_index = self.user_indices[row[0]]
                col_index = self.VIP_indices[row[1]]
                self.matrix[row_index][col_index] = True
            self.VIP_pops = self.matrix.mean(axis=0)

    '''
    Function to retrieve the user similarities.
    '''
    def get_user_similarities(self):
        with open('Twitter2014/user_similarity.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            for row in csv_reader:
                if row[0] not in self.similar_users:
                    self.similar_users[row[0]] = list()
                self.similar_users[row[0]].append((row[1], row[2]))

    '''
    Recommend a VIP based on user similarities.
    '''
    def recommend_user_based(self, user, solution=False, **kwargs):
        if "num_s_users" not in kwargs:
            kwargs["num_s_users"] = 10
        # get the users vector
        user_vector = self.matrix[self.user_indices[user]]
        # Get all the similar users and their similarity values
        similar_users = self.similar_users[user]
        similar_users.sort(key=itemgetter(1), reverse=True)
        # Get the usernames of the "num_s_users" most similar users
        usernames = list(zip(*similar_users[:kwargs["num_s_users"]]))[0]
        # Get the row indices of those users and build a submatrix with them
        row_indices = [self.user_indices[name] for name in usernames]
        s_matrix = self.matrix[row_indices, :]
        # Average the columns of that matrix to get the probabilities of the
        # average similar user liking each VIP
        s_centroid = s_matrix.mean(axis=0)
        # Sort that array to suggest 10 VIPs that the user doesnt already follow
        recommendations = list()
        guess_correct = False
        for idx in s_centroid.argsort()[::-1]:
            if len(recommendations) == 10:
                break
            if not user_vector[idx]:
                name = self.VIP_names[idx]
                recommendations.append(name)
                if name == solution:
                    guess_correct = True
        return guess_correct, recommendations


# Function to test a number of tests
def test(R, num_tests=1000, verbose="testing", method="user", **kwargs):
    if verbose == "testing":
        print("Running tests...")
    score = 0
    # Create the output file
    with open('recommender_s2880024.out', 'w+') as output:
        # Read the test data
        with open('Twitter2014/matrix_test.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            # For each row in test data, recommend 10 VIPs and see if we scored
            for idx, row in enumerate(csv_reader):
                if method == "user":
                    res, recs = R.recommend_user_based(row[0], row[1], **kwargs)
                if method == "VIP":
                    res, recs = R.recommend_VIP_based(row[0], row[1], **kwargs)
                if res:
                    score += 1
                rec_string = " ".join([str(VIP) for VIP in recs])
                output_string = f"{row[0]} {row[1]} {rec_string} {int(res)}"
                if verbose == "handing_in":
                    print(output_string)
                else:
                    output.write(f"{output_string}\n")
                if idx == num_tests:
                    break
            if verbose == "handing_in":
                print(score)
            else:
                output.write(str(score))
    # Print the time taken and the final score
    if verbose == "testing":
        print(f"-> Done, after {time.time() - R.start_time}\n")
        if method == "user":
            print(f"Collaborative filtering score: {score}")
        if method == "VIP":
            print(f"Item based recommendation score: {score}")
        print(f"{num_tests} tests in total.")
    return score


if __name__ == "__main__":
    R = Recommender(verbose=False, parse_VIP_sims=False)
    results = test(R, verbose="handing_in")
