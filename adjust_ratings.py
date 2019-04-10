# adjust ratings csv
import csv
with open('data/rating.csv') as csv_file:
	ratings = csv.reader(csv_file, delimiter=',')
	next(ratings, None) # skip the header
	# build dic for user and which shows they watched
	dic = {}
	line_count = 0
	for line in ratings:
		line_count += 1
		user = line[0]
		anime = line[1]
		rating = line[2]
		if user not in dic:
			dic[user] = [tuple((anime, rating))]
		else:
			val = dic[user]
			val.append(tuple((anime, rating)))
			dic[user] = val
	print(line_count)
	# new dic with users that have at least the counter boundary amount of ratings
	at_least_five_ratings_user = {}
	for user, tuplist in dic.items():
		counter = 0
		for anime, rating in tuplist:
			if rating != -1:
				counter += 1
			else: 
				continue
		if counter >= 251:
			at_least_five_ratings_user[user] = tuplist
		else:
			continue
	# invert the dict to look at the amount of ratings per show of users with at least the counter amount of views
	invert_to_anime_id = {}
	for user, tuplist in at_least_five_ratings_user.items():
		for anime_id, rating in tuplist:
			if anime_id not in invert_to_anime_id:
				invert_to_anime_id[anime_id] = [tuple((user, rating))]
			else:
				val = invert_to_anime_id[anime_id]
				val.append(tuple((user, rating)))
				invert_to_anime_id[anime_id] = val
	# filter out shows that have less than the counter amount of views
	at_least_five_ratings_anime = {}
	for anime, tuplist in invert_to_anime_id.items():
		counter = 0
		for user, rating in tuplist:
			if rating != -1:
				counter += 1
			else: 
				continue
		if counter >= 251:
			at_least_five_ratings_anime[anime] = tuplist
		else:
			continue
	print("we here")	
	# set back to original format
	final_list = []
	for anime, user_tup in at_least_five_ratings_anime.items():
		for user, rating in user_tup:
			final_list.append([user, anime, rating])
	print(len(final_list))
	#for i in final_list:
	#	print(i)











			
