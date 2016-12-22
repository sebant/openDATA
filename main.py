# -*- coding: utf-8 -*-
#pip install twython
from twython import Twython
from time import sleep

#Connection----------------------------------------------------------

APP_KEY = 'pIHTSqoX7QzW4HhFPJauhNglA'
APP_SECRET = 'hR4x7xDdWkGkX3NafcXCTeP8Mlk5pH0J9OODKD4T7vPT1LJoQM'
twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

#Query---------------------------------------------------------------

def getListOfSearch():
	catalunya = ["Catalufo", "Catalunya", "Cataluña", "Catalanes", "Catalan", "Catalufos", "Polaco", "Polacos", "Indepe", "Indepes", "Independentista", "Independentistas", "Charnego", "Xarnego", "Txarnego", "Charnegos", "Xarnegos", "Txarnegos", "Catala", "Catalans", "Independentistes"]
	puta = ["Puto", "Putos", "Puta", "Putas", "Mierda", "Hijoputa", "Hijos", "Hijo", "Joputa", "Joputas","Agarrados","Mierdas", "Tacaño", "muertos", "muerte", "morid", "mueran", "murais"]

	allPos = []
	for cat in catalunya:
		for p in puta:
			allPos.append(cat + " " + p)
	return allPos


def scrapNTimes(n):
	t = 0 #Total number of tweet found.
	for search in getListOfSearch():
		print "Searching for: ", search
		for i in range(n):
			try:
				f = open(search.replace(" ", "_")+'.txt', 'a')
				results = twitter.search(count=5000, q=search)
				for result in results["statuses"]:
					#if(result["created_at"] < lastdate)break
					
					t+=1
					print "Tweet GOT! Total:", t

					f.write(result["text"].encode('utf-8').strip())
					f.write(" - " + result["created_at"])
					f.write("\n--------------------------------\n")
				break

			except:
				print "Error occured trying"
				print "Sleeping..."
				sleep(60*15)

def repeatedTweet(tw, search):
	f = open('search.txt', 'r')
	f.readline()


scrapNTimes(10)