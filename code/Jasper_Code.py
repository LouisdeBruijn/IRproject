import csv
from operator import itemgetter
from collections import defaultdict
import time

def create_dataframes():
    '''Opens and reads the required files. Then structures the training file and the similarity file into dictionairies.
     The test data is stored in a list.'''
    
    matrix_file = csv.reader(open('Twitter2014/matrix_training.csv', mode='r'), delimiter=" ")
    user_follow_vips = defaultdict(list)
    for row in matrix_file:
        user_follow_vips[row[0]].append(row[1])

    similarity_file = csv.reader(open('Twitter2014/user_similarity.csv', mode='r'), delimiter=" ")
    user_similarity = defaultdict(list)
    for row in similarity_file:
        user_similarity[row[0]].append((row[1], float(row[2])))
        user_similarity[row[1]].append((row[0], float(row[2])))

    test_file = []
    for line in open('Twitter2014/matrix_test.csv', mode='r').readlines():
        test_file.append((line.rstrip().split()[0], line.rstrip().split()[1]))

    return user_follow_vips, user_similarity, test_file
        
def similar_users(users, n):
    '''Takes a list of tuples which hold the similar users to the test file user and their similarity scores.
    Then sorts the list of tuples on the highest similarity scores. 
    Returns the similar users in a list sorted from highest jaccard score to lowest.'''

    return sorted(users, key=itemgetter(1), reverse=True)[:n]

def sim_users_following(user, top_n_most_sim_users, user_follow_vips):
    '''First finds the vips that the similar users follow.
    Then checks if those vips aren't already followed by the user in question.
    Returns a list of 10 vips that we can recommend to the user to follow.'''

    vips = defaultdict(float)
    for sim_user in top_n_most_sim_users:
        for vip in user_follow_vips[sim_user[0]]:
            vips[vip] += sim_user[1]
    recommend_output = []
    for vip in sorted(vips.items(), key=itemgetter(1), reverse=True):
        if vip[0] not in user_follow_vips[user]:
            recommend_output.append(vip[0])
    return recommend_output[:10]

def main():
    '''Executes the data structuring and the recommendation algorithms.
    Writes lines to .out file consisting of: User Vip Recommended vips and a binary indication of correctly recommended vips.
    The last line of the .out file consists of the number of correctly recommended vips. 
    Lastly, prints the number of correctly recommended vips.'''

    user_follow_vips, user_similarity, test_file = create_dataframes()
    count = 0
    output_name = 'recommender_3196763.out'
    output_file = open(output_name,'w') 
    for row in test_file:
        user = row[0]
        vip = row[1]
        top_n_most_sim_users = similar_users(user_similarity[user], 15)
        top_ten_recommend = sim_users_following(user, top_n_most_sim_users, user_follow_vips)
        
        output_string = user + ' ' + vip
        for recommend_user in top_ten_recommend:
            output_string = output_string + ' ' + recommend_user
        
        if vip in top_ten_recommend:
            count += 1
            output_string = output_string + ' 1'
        else:
            output_string = output_string + ' 0'
        output_file.write(output_string + '\n')

    count_string = str(count)
    output_file.write(count_string)
    print("Number of items recommended correctly: " + count_string)

if __name__ == '__main__':
	main()