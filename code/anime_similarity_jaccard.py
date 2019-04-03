# This program creates/formats the data into the similarity matrix between anime_shows on jaccard

import csv
from collections import defaultdict
from itertools import combinations
import time
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def u(lst1, lst2): 
    final_list = list(set(lst1) | set(lst2)) 
    return final_list 

def get_values_to_csv(dic):
	# get a list of all unique combination pairs
	list_of_keys = []
	for key in dic.keys():
		list_of_keys.append(key)
	pairs = list(combinations(list_of_keys, 2))
	start = time.time()
	# calculate similarities between pairs
	#print(len(pairs))
	counter = 0
	for anime_id1, anime_id2 in pairs:
		users1 = dic.get(anime_id1)
		users2 = dic.get(anime_id2)
		intersect = intersection(users1, users2)
		union = u(users1, users2) 
		# calculate jaccard score
		jaccard = len(intersect)/len(union)
		# calculate cosine similarity
		counter += 1
		if counter == 999:
			break
	end = time.time()
	animes = (end - start)
	print(animes)
		
		

def main():
	# dictionary of AnimeId = users_who watched
	dic = defaultdict(list)
	with open('../data/matrix_user_shows_watched.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		
		next(csv_reader)
		for row in csv_reader:
			user_id = row[0]
			anime_id = row[1]
			value = dic[anime_id]
			dic[anime_id].append(user_id)
	get_values_to_csv(dic)
	

if __name__ == '__main__':
	main()
	
