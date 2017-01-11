# -*- coding: utf-8 -*-


def getAllQueryFileName():
	import os
	return ["scrapResults/"+f for f in os.listdir("scrapResults") if os.path.isfile(os.path.join("scrapResults", f))]



def main():
	import time
	import os
	import json
	import csv
	import codecs

	import sys
	reload(sys)
	sys.setdefaultencoding('utf8')

	#creem la carpeta tables si no existeix
	if(not os.path.exists("tables")):
		os.makedirs("tables")

	#previous searches
	vfileName=getAllQueryFileName()
	
	#no tots els twits tenen les mateixes claus
	#posarem a header totes les possibles claus per poguer escriure correctament
	header=[]
	for fileName in vfileName:
		f = open(fileName)
		queryResultJson =json.load(f)
		f.close()
		for query in queryResultJson:
			if "statuses" in queryResultJson[query]:
				for tweet in queryResultJson[query]["statuses"]:
					header=list(set(header+tweet.keys()))

	#obrim fitxer csv
	vIds =[]
	lJson=[]
	vIdsUsers=[]
	with codecs.open("tables/test.csv", "w", encoding="utf-8") as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=header)
		writer.writeheader()
		#obrim fitxer json
		for fileName in vfileName:
			print fileName
			
			f = open(fileName)
			queryResultJson =json.load(f)
			f.close()

			#per cada busqueda
			for query in queryResultJson:
				#si no te statuses es pq li hem tret al request.py 
				#ja que tots els resultats estan en la seguent busqueda
				if "statuses" in queryResultJson[query]:
					for tweet in queryResultJson[query]["statuses"]:
						if tweet["id"] not in vIds:
							writer.writerow(tweet)
							lJson.append(tweet)
							vIds.append(tweet["id"])
							if tweet["user"]["id"] not in vIdsUsers:
								vIdsUsers.append(tweet["user"]["id"])

	import pickle
	with open("tables/all.bin","wb") as f:
		pickle.dump(lJson,f)
	with open("tables/usersIds.bin","wb") as f:
		pickle.dump(vIdsUsers,f)

						
if __name__ == "__main__":
    main()
