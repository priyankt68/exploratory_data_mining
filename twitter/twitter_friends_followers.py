# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Data Mining on Twitter
# --------------------------------------------------

# <markdowncell>

# In this Ipython Notebook, I'll try to explore data mining on Twitter using [Twitter API v1.1](http://dev.twitter.com).

# <markdowncell>

# ### Importing the required modules

# <codecell>

import twitter
import sys
import getopt
import json
import csv
import pandas as pd
from pandas.io.parsers import ExcelWriter
from pandas.io.parsers import ExcelFile




# <markdowncell>

# ### Authentication & Authorization
# * The very first step in using [ Twitter API calls](https://dev.twitter.com/docs)is to perform oAuth Dance procedure for authentication purposes.
# * [Twitter API calls](https://dev.twitter.com/docs)
#  * [twitter.oauth.OAuth(access_key,access_secret,consumer_key,consumer_secret)](https://dev.twitter.com/docs/auth)
#  

# <codecell>

def oauth_login():
	
	consumer_key = "xx"
	consumer_secret = "xx"
	access_key = "xx"
	access_secret = "xx"
	auth = twitter.oauth.OAuth(access_key,access_secret,consumer_key,consumer_secret)

	twitter_api = twitter.Twitter(auth=auth)

	return twitter_api

# <markdowncell>

# ### Following Information
# 
# * Procedure to retrieve friends or twitter handles a specified one follows
# * [ Twitter API calls](https://dev.twitter.com/docs)
#   * [ twitter_api.users.lookup() ](https://dev.twitter.com/docs/api/1/get/users/lookup)

# <codecell>

def friends_ids(username):
	quey = twitter_api.friends.ids(screen_name = username)
	return quey;


### Returns the friends' complete information for an input twitter handle

def friends_info(username):
	result=[]
	query = friends_ids(username)

	for n in range(0, len(query["ids"]), 100):
		ids = query["ids"][n:n+100]

	#creating a sub-query , storing more information about these users
		sub_query = twitter_api.users.lookup(user_id = ids)
    
    # checking for verified accounts and then updating the verified parameter
		for user in sub_query:  
			verified=" "
			if user["verified"]:
				verified= "*"

	if 'next_cursor' in sub_query:
		next_cursor = sub_query['next_cursor']
	else:
		next_cursor = 0
	if 'previous_cursor' in sub_query:
		previous_cursor = sub_query['previous_cursor']
	else:
		previous_cursor = 0

	while True:
		result +=[(x) for x in sub_query]
		if next_cursor == 0 or next_cursor == previous_cursor:
			break
		else:
			cursor = next_cursor

	return pd.DataFrame(result)  ## Storing it as a pandas dataframe

# <markdowncell>

# ### Followers Information
# * Procedure to retrieve followers information for a specified twitter handle. 
# -  [ Twitter API calls](https://dev.twitter.com/docs)
#   * [ twitter_api.followers.ids()](https://dev.twitter.com/docs/api/1/get/followers/ids)
#   * [ twitter_api.users.lookup() ](https://dev.twitter.com/docs/api/1/get/users/lookup)

# <codecell>

### Returns the friends' complete information for an input twitter handle
def followers_info(username,cursor = -1):
	result=[]
	
	while(cursor != 0):
		query = twitter_api.followers.ids(screen_name = username, cursor = cursor, count = 200)
		for ids in query["ids"]:
			sub_query = twitter_api.users.lookup(user_id = ids)
			for user in sub_query:
				verified=" "
				if user["verified"]:
					verified = "*"
			
			result += [(x) for x in sub_query]

		cursor = query['next_cursor']

	return pd.DataFrame(result)




# <codecell>
def main(argv):
	username = ''
	try:
		args = getopt.getopt(argv,'')
	except getopt.GetoptError:
		print "filename.py <twitter_handle>"
		sys.exit(2)

	return args[1];
# <codecell>
# <markdowncell>

# * Main function to make the function calls for and accepting [Pandas](http://pandas.pydata.org) dataframes for results
# 
# PS: Since python doesn't have a defined entry point in contrast with other object-oriented languages like C++,Java; " __name__ == __main__ " doesn the equivalent activity
# <markdowncell>

# <codecell>
if __name__ == "__main__":

	twitter_api = oauth_login()
	reload(sys)
	
	sys.setdefaultencoding("utf-8")
	
	username = ''.join(main(sys.argv[1:]))
		
	filename = username + ".csv"

	friends = pd.DataFrame(friends_info(username), columns = ["screen_name", "name","description", "favourites_count", "followers_count", "following", "friends_count", "location",  "profile_image_url", "profile_image_url_https", "time_zone", "url"]);
	friends.to_csv("data/" + username+"_friends.csv", sep = "," , header = "True" , index = "True");

	followers = pd.DataFrame(followers_info(username),columns = ["screen_name", "name","description", "favourites_count", "followers_count", "following", "friends_count", "location",  "profile_image_url", "profile_image_url_https", "time_zone", "url"] )		
	followers.to_csv("data/" + username+"_followers.csv", sep = "," , header = "True" , index = "True");
	

# <codecell>

