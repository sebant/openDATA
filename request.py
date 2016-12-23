# -*- coding: utf-8 -*-
#pip install twython

def getListOfSearch():
	catalunya = ["Catalufo", "Catalunya", "Cataluña", "Catalanes", "Catalan", "Catalufos", "Polaco", "Polacos", "Indepe", "Indepes", "Independentista", "Independentistas", "Charnego", "Xarnego", "Txarnego", "Charnegos", "Xarnegos", "Txarnegos", "Catala", "Catalans", "Independentistes"]
	puta = ["Puto", "Putos", "Puta", "Putas", "Mierda", "Hijoputa", "Hijos", "Hijo", "Joputa", "Joputas","Agarrados","Mierdas", "Tacaño", "muertos", "muerte", "morid", "mueran", "murais"]

	return [cat+" "+p for cat in catalunya for p in puta]

def connect():
	from twython import Twython
	
	APP_KEY = 'pIHTSqoX7QzW4HhFPJauhNglA'
	APP_SECRET = 'hR4x7xDdWkGkX3NafcXCTeP8Mlk5pH0J9OODKD4T7vPT1LJoQM'
	twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
	ACCESS_TOKEN = twitter.obtain_access_token()
	twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

	return twitter

def scrapNTimes(twitter,n,search):
	import time
	#Query---------------------------------------------------------------

	for i in range(n):
		try:
			results = twitter.search(count=5000, q=search)
			print "Total number of tweet found: ", len(results["statuses"])
			
			if(len(results["statuses"])==0):
				break



			if(len(results["statuses"])>=100):
				print search, "hem trobat 100 tuits nous !!!!!!"
			return results

		except:
			print "Error occured trying"
			print "Sleeping..."
			time.sleep(60*15)
		

def main():
	import time
	import os
	import json
	
	#creem la carpeta scrapResults si no existeix
	if(not os.path.exists("scrapResults")):
		os.makedirs("scrapResults")

	#conectem
	twitter = connect()

	#nom del fitxer ANY MES DIA_HORA MINUT SEGON
	fileName = "scrapResults/"+time.strftime("%Y%m%d_%H%M%S", time.gmtime())+".txt"
	f = open(fileName, 'w')
	
	for search in getListOfSearch():
		print "Searching for: ", search
		#10 nombre dintents que fer per reconectar en cada busqueda
		results = scrapNTimes(twitter,10,search)
		json.dump(results, f)	
		
if __name__ == "__main__":
    main()
