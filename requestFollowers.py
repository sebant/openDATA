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

def scrap(twitter, listUsersIds, dict2Ret,fileout,vUsers2F):
	#Query---------------------------------------------------------------
	import time
	import pickle
	import datetime
	import sys
	from twython import TwythonError, TwythonRateLimitError, TwythonAuthError
		
	for index, userId in enumerate(listUsersIds):
		print str(userId) + " \t " + str(index) + "/" + str(len(listUsersIds))
		i=0
		fail=False
		while(str(userId) not in dict2Ret and not fail and not str(userId) in vUsers2F and not userId in vUsers2F):
			i+=1
			print str(userId) + "\ttry: " + str(i)
			
			try:
				dict2Ret[str(userId)] = twitter.get_followers_ids(user_id = userId)
				saveAndWait(fileout,dict2Ret)
			except TwythonRateLimitError as e:
				print "TwythonRateLimitError"
				fail=True
				#rate superat
				if int(e.error_code) == 429:
					print "Superat el ratio 1 x min, esperem 15 minuts"
					print "Si cap de nos esta executant el programa des dun altre pc hem de canviar les credencials"
					#lerror hauria de contindre el temps que falta
					time.sleep(60*60*15)
					fail = False
					#el tornem a buscar
				else:
					print e
					time.sleep(60)
					
			except TwythonAuthError as e:
				print "TwythonAuthError"
				fail=True
				if int(e.error_code) == 401:
					pathUsers2follow = "tables/users2follow.bin"
					vUsers = load(pathUsers2follow,[])
					if userId not in vUsers:
						vUsers.append(userId)
						import pickle
						with open(pathUsers2follow,"wb") as f:
							pickle.dump(vUsers,f)

					print "posible motiu: usuari amb perfil protegit"
					print "to do: fer amb laltra conexio"
					time.sleep(60)
				else:
					print e
				time.sleep(60)
			except TwythonError as e:
				print "TwythonError"
				fail=True
				try:
					if int(e.error_code) == 404:
						print "Usuari eliminat, el posem a la llista amb un seguidor -1"
						dict2Ret[str(userId)] = {"ids":[-1]}
						saveAndWait(fileout,dict2Ret)
					else:
						print e
						time.sleep(60)
				except:
					print e
					time.sleep(60)
					
			except:
				fail=True
				print ""
				print "Error: " + str(sys.exc_info()[0])
				print ""
				time.sleep(60)

	return [1,dict2Ret]

def saveAndWait(filename,data):
	import pickle
	import time
	import datetime
	import sys
	try:
		bfsave = datetime.datetime.now()
		
		with open(filename,"wb") as f:
			pickle.dump(data,f)
		
		savingTime = datetime.datetime.now() - bfsave
		dif = 60-savingTime.total_seconds()
		print "waiting: " + str(dif)
		if dif > 0:
			time.sleep(dif+1)
	except:
		print "saveAndWait Error: " + str(sys.exc_info()[0])
			

def main():
	import os
	import pickle
	
	print "start main"

	fileout = "scrapFollResults/followsConexions.bin"
	filein = fileout
	fileListIdsIn = "tables/usersIds.bin"

	#creem la carpeta scrapResults si no existeix
	if(not os.path.exists("scrapFollResults")):
		os.makedirs("scrapFollResults")

	print "read prev res"
	#carregeuem els que ja tenim
	dic2res =load(filein,{})
	print "prev res readed"

	#llegim llista
	print "read users to req"
	lUsersIds = load(fileListIdsIn,[])	
	print "users to req readed"

	print "read usrers wrong"
	pathUsers2follow = "tables/users2follow.bin"
	vUsers2F = load(pathUsers2follow,[])
	print "users wrong readed"
	
	print "conect to twitter"
	#conectem
	twitter = connect()
	print "twitter conected"

	print "start scrap"
	dic2res = scrap(twitter,lUsersIds,dic2res,fileout,vUsers2F)
	
	#guardem
	save(fileout,dic2res)
	
	for i in range(10):
		print "!!!!!!!!!!!!!!!!FINISH!!!!!!!!!!!!!!!!!!"

if __name__ == "__main__":
    main()
