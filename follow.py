def connect2():
	from twython import Twython
	APP_KEY = 'pIHTSqoX7QzW4HhFPJauhNglA'
	APP_SECRET = 'hR4x7xDdWkGkX3NafcXCTeP8Mlk5pH0J9OODKD4T7vPT1LJoQM'
	
	twitter = Twython(APP_KEY, APP_SECRET)
	auth = twitter.get_authentication_tokens()

	#{u'oauth_token_secret': u'EZCPEc5x6bncqnl4z1cyDz5136UPCN9a', 
	#'auth_url': 'https://api.twitter.com/oauth/authenticate?oauth_token=NltG6gAAAAAAydthAAABWaMwqEg', 
	#u'oauth_token': u'NltG6gAAAAAAydthAAABWaMwqEg', 
	#u'oauth_callback_confirmed': u'true'}

	OAUTH_TOKEN = auth['oauth_token']
	OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
	OAUTH_URL = auth["auth_url"]
	
	print OAUTH_URL
	variable = raw_input('input PIN CODE!: ')	
	
	twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	final_step = twitter.get_authorized_tokens(int(variable))
	
	OAUTH_TOKEN = final_step['oauth_token']
	OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']
	
	twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	
	return twitter


def load(filename,retdef):
	import os
	import pickle
	
	if(not os.path.isfile(filename)):
		print "File "+filename+ " does not exist"
		return retdef

	with open(filename, "rb") as binFile:
		return pickle.load(binFile)

def main():
	from twython import TwythonError, TwythonRateLimitError, TwythonAuthError
	
	twitter= connect2()
	
	path = "tables/users2follow.bin"
	vUsers = load(path,[])
	
	for user in vUsers:
		print user		
		try:
			twitter.create_friendship(user_id=user,follow=True)
		except TwythonError as e:
			print e

if __name__ == "__main__":
    main()


'''{u'follow_request_sent': True
 u'has_extended_profile': False
 u'profile_use_background_image': True
 u'default_profile_image': False
 u'id': 774314204828499969
 u'profile_background_image_url_https': None
 u'verified': False
 u'translator_type': u'none'
 u'profile_text_color': u'333333'
 u'muting': False
 u'profile_image_url_https': u'https://pbs.twimg.com/profile_images/819567389230698498/Z-I6SnNw_normal.jpg'
 u'profile_sidebar_fill_color': u'DDEEF6'
 u'entities': {u'description': {u'urls': []}}
 u'followers_count': 29
 u'profile_sidebar_border_color': u'C0DEED'
 u'id_str': u'774314204828499969'
 u'profile_background_color': u'F5F8FA'
 u'listed_count': 1
 u'is_translation_enabled': False
 u'utc_offset': None
 u'statuses_count': 6240
 u'description': u'weno'
 u'friends_count': 97
 u'location': u' Conchinchina'
 u'profile_link_color': u'1DA1F2'
 u'profile_image_url': u'http://pbs.twimg.com/profile_images/819567389230698498/Z-I6SnNw_normal.jpg'
 u'following': False
 u'geo_enabled': False
 u'profile_banner_url': u'https://pbs.twimg.com/profile_banners/774314204828499969/1483411260'
 u'profile_background_image_url': None
 u'screen_name': u' '
 u'lang': u'es'
 u'profile_background_tile': False
 u'favourites_count': 506
 u'name': u'Max Power'
 u'notifications': False
 u'url': None
 u'created_at': u'Fri Sep 09 18:31:07 +0000 2016'
 u'contributors_enabled': False
 u'time_zone': None
 u'protected': True
 u'default_profile': True
 u'is_translator': False}
'''