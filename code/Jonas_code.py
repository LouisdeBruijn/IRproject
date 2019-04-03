# recommender_2698617.py
# author: Jonas Schuitemaker
# assignment 3 information retrieval 2018-2019

import csv
import time

# function to load in the n highest user similarities per user into a dict
# dict[user1] = (user2, similarity_score)
def get_user_similarity(n):
	with open('./Twitter2014/user_similarity.csv', mode = 'r') as csv:
		user_similarity = {}
		for line in csv:
			line = line.rstrip().split()
			user_main = line[0]
			user_compare = line[1]
			jaccard = line[2]
			if user_main in user_similarity:
				val = user_similarity.get(user_main)					
				val.append(tuple((user_compare, jaccard)))
				user_similarity[user_main] = val
			else:
				val_list = []
				val_list.append(tuple((user_compare, jaccard)))
				user_similarity[user_main] = val_list
			# also put the mentions of the user2 as user in the dict as there are only bob-ada and not ada-bob similarity scores
			if user_compare in user_similarity:
				val = user_similarity.get(user_compare)
				val.append(tuple((user_main, jaccard)))
				user_similarity[user_compare] = val
			else:
				val_list = []
				val_list.append(tuple((user_main, jaccard)))
				user_similarity[user_compare] = val_list
		# only take the n most similar users
		for key, value in user_similarity.items():
			sorted_by_second = sorted(value, key=lambda tup: tup[1], reverse = True)
			user_similarity[key] = sorted_by_second[:(n)]
		time_to_process_one_user = time.time()
				
		return user_similarity
	
# function to load in users and which VIPS they follow into a dict
# dict[user] = list_of_vips
def get_user_VIP_pair():
	with open('./Twitter2014/matrix_training.csv', mode = 'r') as csv:
		follow = {}
		user_VIP_list = []
		for line in csv:
			line = line.rstrip().split()
			user_main = line[0]
			user_VIP = line[1]
			if user_main in follow:
				VIP_list = follow.get(user_main)				
				VIP_list.append(user_VIP)
				follow[user_main] = VIP_list
			else:
				VIP_list = []
				VIP_list.append(user_VIP)
				follow[user_main] = VIP_list
			user_VIP_list.append(line)
			
		return follow, user_VIP_list

# function to calculate mean score for user in order to centre the scores
def get_average(vips_sim_user, all_recomended_vips):
	follows = 0
	total_suggestions = len(all_recomended_vips)
	for item in all_recomended_vips:
		if item in vips_sim_user:
			follows += 1

	user_mean = follows/total_suggestions
	return user_mean

def main():
	# start measuring program runtime
	'''start = time.time()'''
	# define the amount of users the system will use to make the predicition on
	# i chose ten since it seemed to be were the program settled and runtime was okay
	# (n = 8 had ten less good suggestions eventhough runtime was ~ 25 seconds faster)
	n = 10
	# load in the user similarity data into a dictionary
	user_similarity_dic = get_user_similarity(n)
	
	# load in the training matrix data into a dictionary			
	user_VIP_dic, lines_in_file = get_user_VIP_pair()
	users = []
	for line in lines_in_file:
		users.append(line[0])
	
	# create a list of all users
	users = set(users)
	# initialize dictionary that will have recommended VIPs per user
	recomendation_per_user = {}
	for user in users:
		all_recomended_vips = []
		user_vip_recommendations = {}
		# take users that user is similar to
		similar_users = user_similarity_dic.get(user)
		for sim_user, score in similar_users:
			# take VIPS followed by similar users
			vip_list = user_VIP_dic.get(sim_user)
			all_recomended_vips.append(vip_list)
		all_recomended_vips = [j for i in all_recomended_vips for j in i]

		# take list of possible vips that are recomended
		all_recomended_vips = set(all_recomended_vips)

		# calculate mean score for user in order to centre the scores
		user_vips = user_VIP_dic.get(user)
		vips_to_recommend = []
		follows = 0
		total_suggestions = len(all_recomended_vips)
		for item in all_recomended_vips:
			if item in user_vips:
				follows += 1
			else:
				vips_to_recommend.append(item)
		user_mean = follows/total_suggestions
			
		# calculate recomendation score for vips that user does not follow yet		
		recomendation_scores = {}
		for sim_user, score in similar_users:
			# get vips that the similar user follows
			vips_sim_user = user_VIP_dic.get(sim_user)
			# get average score for similar user
			sim_average = get_average(vips_sim_user, all_recomended_vips)
			# make prediction for recomended users by building weighted function
			for vip in vips_to_recommend:
				if vip in vips_sim_user:
					# build the function to evaluate later from dictionary
					if vip not in recomendation_scores:
						recomendation_scores[vip] = tuple((" ((1 - {})*{})".format(sim_average, score), "{}".format(score)))
					else:
						numerator, denominator = recomendation_scores.get(vip)
						new_num = numerator + " + ((1 - {})*{})".format(sim_average, score)
						new_denom = denominator + " + {}".format(score)
						recomendation_scores[vip] = tuple((new_num, new_denom))
				else:
					if vip not in recomendation_scores:
						recomendation_scores[vip] = tuple((" ((0 - {})*{})".format(sim_average, score), "{}".format(score)))
					else:
						numerator, denominator = recomendation_scores.get(vip)
						new_num = numerator + " + ((0 - {})*{})".format(sim_average, score)
						new_denom = denominator + " + {}".format(score)
						recomendation_scores[vip] = tuple((new_num, new_denom))
		# for each user build a short dictionary containing dict[vip] = weighted evaluated score
		recomendation_scores_evaluated = {}	
		for key, value in recomendation_scores.items():
			nominator, denominator = value
			nom_eval = eval(nominator)
			denom_eval = eval(denominator) 
			recomendation_scores_evaluated[key] = (user_mean + (nom_eval/denom_eval))
		
		# only take the 10 best recomended VIPs per user and build a dictionary
		# dict[user] = list_of_ten_best_recomended_vips	
		ten_recomended_vips = []
		counter = 0
		for w in sorted(recomendation_scores_evaluated, key = recomendation_scores_evaluated.get, reverse = True):
			if counter <= 9:
				ten_recomended_vips.append(w)
				counter +=1
		recomendation_per_user[user] = ten_recomended_vips
	results = []
	# evaluate program on test data and write to csv
	with open('./Twitter2014/matrix_test.csv', mode = 'r') as csv:
		counter = 0
		for line in csv:
			line = line.rstrip().split()
			user = line[0]
			vip = line[1]
			suggestions = recomendation_per_user.get(user)
			su_string = ' '.join(suggestions)	
			if vip in suggestions:
				counter += 1		
				print("{} {} {} {}".format(user, vip, su_string, 1))
				continue	
			else:		
				print("{} {} {} {}".format(user, vip, su_string, 0))

	# also print the total results to the terminal
	print(counter)
	# get the runtime of the program		
	'''
	end = time.time()		
	print(end-start)
	'''


if __name__ == '__main__':
	main()
	
