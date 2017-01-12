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

def load(filename,retdef):
	import os
	import pickle
	
	if(not os.path.isfile(filename)):
		print "File "+filename+ " does not exist"
		return retdef

	with open(filename, "rb") as binFile:
		return pickle.load(binFile)

def scrap(twitter, listUsersIds, dict2Ret,fileout):
	#Query---------------------------------------------------------------
	import time
	import pickle
					
	for userId in listUsersIds:
		print userId
		i=0
		while(str(userId) not in dict2Ret):
			i+=1
			print str(userId) + " try: " + str(i)
			try:
				dict2Ret[str(userId)] = twitter.get_followers_ids(user_id = userId)
			except:
				#GUARDEM
				save(fileout,dict2Ret)
				
				print "Conexio perduda wait 15 minuts "
				time.sleep(60*15+1)
				print "Tornemi"

	return [1,dict2Ret]

def save(filename,data):
	import pickle
	with open(filename,"wb") as f:
		pickle.dump(data,f)
	
def main():
	import os
	
	fileout = "scrapFollResults/followsConexions.bin"
	filein = fileout
	fileListIdsIn = "tables/usersIds.bin"

	#creem la carpeta scrapResults si no existeix
	if(not os.path.exists("scrapFollResults")):
		os.makedirs("scrapFollResults")
	
	#llegim llista
	lUsersIds = load(fileListIdsIn,[])	

	#carregeuem els que ja tenim
	dic2res =load(filein,{})

	#conectem
	twitter = connect()
	
	dic2res = scrap(twitter,lUsersIds,dic2res,fileout)
	
	#guardem
	save(fileout,dic2res)
	
	for i in range(10)
		print "!!!!!!!!!!!!!!!!FINISH!!!!!!!!!!!!!!!!!!"

if __name__ == "__main__":
    main()
