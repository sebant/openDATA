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

def getListUsersIds():
	import os
	filename = "tables/usersIds.bin"
	if(not os.path.isfile(filename)):
		print "File "+filename+ " does not exist"
		return []

	import pickle
	with open(filename, "rb") as binFile:
		return pickle.load(binFile)

	

def scrap(twitter, listUsersIds):
	#Query---------------------------------------------------------------
	dict2Ret = {}
	for userId in listUsersIds:
		print userId

		try:
			dict2Ret[str(userId)] = twitter.get_followers_ids(user_id = userId)
		except:
			print "Conexio perduda wait 16 minuts "
			import time
			time.sleep(60*60*16)
			print "Tornemi"
			try:
				dict2Ret[str(userId)] = twitter.get_followers_ids(user_id = userId)
			except:
				print "no hi ha manera"
				return [0,dict2Ret]
	return [1,dict2Ret]

def main():
	import time
	import os
	import json
	
	#creem la carpeta scrapResults si no existeix
	if(not os.path.exists("scrapFollResults")):
		os.makedirs("scrapFollResults")
	
	#llegim llista
	lUsersIds = getListUsersIds()	

	#conectem
	twitter = connect()
	[allDone,dic2res] = scrap(twitter,[lUsersIds[0]])
	
	#guardem
	import pickle
	with open("scrapFollResults/followsConexions.json","wb") as f:
		pickle.dump(dic2res,f)
		
if __name__ == "__main__":
    main()
