# -*- coding: utf-8 -*-
#pip install twython


def getLastQueryFileName():
	import os
	onlyfiles = [f for f in os.listdir("scrapResults") if os.path.isfile(os.path.join("scrapResults", f))]
	if len(onlyfiles)==0:
		prevResults = False
		dayLast=""
		hourLast=""
	else:
		prevResults = True
		[dayLast,hourLast] = onlyfiles[0].split(".")[0].split("_")
		for file in onlyfiles:
			[day,hour] = file.split(".")[0].split("_")
			if(int(day)>int(dayLast)):
				dayLast = day
				hourLast = hour
			elif(int(day) == int(dayLast)):
				if(int(hour)>int(hourLast)):
					dayLast = day
					hourLast = hour
	return [prevResults,"scrapResults/"+dayLast+"_"+hourLast+".json"]

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

def scrapNTimes(twitter,n,search,lastResults):
	#Query---------------------------------------------------------------
	for i in range(n):
		try:
			results = twitter.search(count=5000, q=search)
			print search, "\ttotal number of tweet found: ", len(results["statuses"])
			
			if(len(results["statuses"])==0):
				return [1,results]
			
			if "statuses" in lastResults:
				elements2Delete=[]
				for result in results["statuses"]:
					for lastresult in lastResults["statuses"]:
						if(result["id"]==lastresult["id"]):
							elements2Delete.append(lastresult)
				
				for element in elements2Delete:
					lastResults["statuses"].pop(lastResults["statuses"].index(element))
				
				if(len(lastResults["statuses"])>=100 ):
					print ""
					print ""
					print search, "!!!!!! HEM PERDUT TUITS !!!!!! AUGMENTAR FREQUENCIA"
					print ""
					print ""
					import time
					time.sleep(10)

			return [1,results]

		except:
			return [0,0]

def main():
	import time
	import os
	import json
	
	#creem la carpeta scrapResults si no existeix
	if(not os.path.exists("scrapResults")):
		os.makedirs("scrapResults")

	#conectem
	twitter = connect()
	
	#previous search
	[lastExist, fileNameLast]=getLastQueryFileName()
	if lastExist:
		#print "Last query is: ", fileNameLast
		fL = open(fileNameLast)
		lastResult=json.load(fL)
		fL.close()
	else:
		lastResult={}
		for search in getListOfSearch():
			lastResult[search]={}

	
	dicResults = {}
	for search in getListOfSearch():
		#print "Searching for: ", search
		#10 nombre dintents que fer per reconectar en cada busqueda
		[queryDone,results] = scrapNTimes(twitter,10,search,lastResult[search])
		if queryDone:
			dicResults[search]=results
		else:
			print "ERROR DE CONEXIO"
			time.sleep(60*15)
			twitter = connect()
			[queryDone,results] = scrapNTimes(twitter,10,search,lastResult[search])
			if queryDone:
				print "ERROR DE CONEXIO ARRETGLAT"
				dicResults[search]=results
			else:
				print "ERROR DE CONEXIO PERSISTEIX"
				dicResults[search]={}
	
	#nom del fitxer ANY MES DIA_HORA MINUT SEGON
	fileName = "scrapResults/"+time.strftime("%Y%m%d_%H%M%S", time.gmtime())+".json"
	f = open(fileName,"w")
	json.dump(dicResults, f)	

	if lastExist:
		fL = open(fileNameLast,"w")
		json.dump(lastResult, fL)	


		
if __name__ == "__main__":
    main()
