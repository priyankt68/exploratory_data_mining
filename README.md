Exploratory Data Mining
=======================

My experiments in Exploratory Data Mining on various social networking sites such as Twitter, Reddit, Facebook and LinkedIn

## Twitter


### Importing the required modules


    import twitter
    import sys
    import json
    import csv
    import pandas as pd

### Authentication & Authorization
* The very first step in using [ Twitter API
calls](https://dev.twitter.com/docs)is to perform oAuth Dance procedure for
authentication purposes.
* [Twitter API calls](https://dev.twitter.com/docs)
 * [twitter.oauth.OAuth(access_key,access_secret,consumer_key,consumer_secret)](https://dev.twitter.com/docs/auth)

    def oauth_login():
    	consumer_key = "xx"
    	consumer_secret = "xx"
    	access_key = "xx"
    	access_secret = "xx"
    	auth = twitter.oauth.OAuth(access_key,access_secret,consumer_key,consumer_secret)
    	twitter_api = twitter.Twitter(auth=auth)
    	return twitter_api
    

### Following Information

* Procedure to retrieve friends or twitter handles a specified one follows
* [ Twitter API calls](https://dev.twitter.com/docs)
  * [ twitter_api.users.lookup()](https://dev.twitter.com/docs/api/1/get/users/lookup)

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

### Followers Information
* Procedure to retrieve followers information for a specified twitter handle.
-  [ Twitter API calls](https://dev.twitter.com/docs)
  * [ twitter_api.followers.ids()](https://dev.twitter.com/docs/api/1/get/follow
ers/ids)
  * [ twitter_api.users.lookup()](https://dev.twitter.com/docs/api/1/get/users/lookup)

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
    

* Main function to make the function calls for and accepting
[Pandas](http://pandas.pydata.org) dataframes for results
PS: Since python doesn't have a defined entry point in contrast with other
object-oriented languages like C++,Java; " __name__ == __main__ " doesn the
equivalent activity


    
    
    if __name__ == "__main__":
    	twitter_api = oauth_login()
    	reload(sys)
    	sys.setdefaultencoding("utf-8")
    	### finding friends of a particular username
    	priyank_friends = friends_info("priyankt68")
        ### finding followers of a particular username
    	priyank_followers = followers_info("priyankt68")
    	
    	


    
