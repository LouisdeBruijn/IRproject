import numpy as np


data = np.load('user_cosine_similarities.npy')
data2 = np.load('user_utility_matrix.npy')

for row in data:
    where = np.where(row<0.9)
    new_data = row[where]
    maximum = np.amax(new_data)
    index = np.where(data == maximum)

    #print(maximum) This is the cosine score of most similar user.
    #print(index)   This is the numpy array index of the most similar user.