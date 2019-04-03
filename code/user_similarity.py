from collections import defaultdict
from itertools import combinations
import csv
import time


def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def union(lst1, lst2): 
    final_list = list(set(lst1) | set(lst2)) 
    return final_list 


def jaccard(user_anime, users):
    for user1 in users[:5]:
        anime_watched = user_anime[user1]
        for user2, anime in user_anime.items():
            if user1 != user2:
                intersect = intersection(anime_watched, anime)
                un = union(anime_watched, anime)
                if len(intersect) != 0:
                        jaccard = len(intersect)/len(un)
                        print(user1, user2, jaccard)


def main():
    start = time.time()
    ratings_file = csv.reader(open('data/rating.csv', mode='r'), delimiter=",")
    user_anime = defaultdict(list)
    users = []
    next(ratings_file)
    for row in ratings_file:
        user_id = int(row[0])
        anime_id = int(row[1])
        user_anime[user_id].append(anime_id)
        users.append(user_id)
    users = set(users)
    users = sorted(users)
    jaccard(user_anime, users)
    
    
    end = time.time()
    print(end - start)
if __name__ == '__main__':
	main()    