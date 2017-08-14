# Programmer: Me
# Version: 1.0
# Purpost: Scan /r/medicine and retrieve Respiratory related articles posted.

#TODO:
	# -Add a date/time stamp
	# -Auto post articles to a RT group

import praw
import rt_config
import time
import os
#import datetime

# Log the bot in using rt_config.py
def bot_login():
	print("Logging in...")
	#gets login and password from a config file.
	r = praw.Reddit(username = rt_config.username,
				password = rt_config.password,
				client_id = rt_config.client_id,
				client_secret = rt_config.client_secret,
				user_agent = "Get Articles related to Respiratory Therapy from /r/medicine v1.0")
	print("Logged in...")

	return r


# Run the bot to get articles
def run_bot(r, rt_articles, rt_search_terms):
	for submission in r.subreddit('medicine').new(limit=25):
		for term in rt_search_terms:
			title = submission.title.split()
			title = [item.lower() for item in title]
			if term in title and submission.url not in rt_articles:
				print("Found a title with ", term, submission.title)
				with open ("rt_articles.txt", "a") as f:
							f.write(submission.title + "\n")
							f.write(submission.url + "\n")
							f.write("\n")
	
	#print(rt_articles)
	print("Sleeping for 30 Secs...")
	#Sleep for 30 min
	time.sleep(30)


# Get the already found articles URL's saved in the text file
def get_saved_articles():
	if not os.path.isfile("rt_articles.txt"):
		rt_articles = []
	else:
		with open("rt_articles.txt", "r") as f:  #"r" means reading the file
			rt_articles = f.read()
			rt_articles = rt_articles.split("\n")
			
	return rt_articles


# Get the terms to search for in posted articles
def get_search_terms():
	if not os.path.isfile("rt_search_terms.txt"):
		rt_search_terms = []
	else:
		with open("rt_search_terms.txt", "r") as f:  #"r" means reading the file
			rt_search_terms = f.read()
			rt_search_terms = rt_search_terms.split("\n")
			
	return rt_search_terms


r = bot_login()

rt_search_terms = get_search_terms()

while(True):	
	rt_articles = get_saved_articles()	
	run_bot(r, rt_articles, rt_search_terms)