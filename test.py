# -*- coding: utf-8 -*-
#pip install twython


def connect():
	from twython import Twython
	
	APP_KEY = 'pIHTSqoX7QzW4HhFPJauhNglA'
	APP_SECRET = 'hR4x7xDdWkGkX3NafcXCTeP8Mlk5pH0J9OODKD4T7vPT1LJoQM'
	twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
	ACCESS_TOKEN = twitter.obtain_access_token()
	twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

	return twitter

			
			
def main():
	twitter = connect()
	res = twitter.get_followers_ids(screen_name = "ANCDones")
	print res 
	
if __name__ == "__main__":
    main()
