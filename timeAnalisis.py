def main():
	import os
	filename = "tables/all.bin"
	if(not os.path.isfile(filename)):
		print "File "+filename+ " does not exist"
		return

	import pickle
	with open(filename, "rb") as binFile:
		lTweets = pickle.load(binFile)

	from datetime import datetime
	
	slTweets = sorted(lTweets , key=lambda tweet: datetime.strptime(tweet["created_at"],"%a %b %d %H:%M:%S +0000 %Y"))

	import time
	for tweet in slTweets:
		tweet["created_at"] = time.strptime(tweet["created_at"],"%a %b %d %H:%M:%S +0000 %Y")
	

	#agrupem per dies
	vTxD=[]
	vTxDp=[]
	vD=[]
	actualDay = slTweets[0]["created_at"].tm_mday
	actualMonth = slTweets[0]["created_at"].tm_mon
	numToday = 0
	ponToday = 0
	for tweet in slTweets:
		if tweet["created_at"].tm_mday == actualDay:
			numToday=numToday+1
			ponToday=ponToday+tweet["user"]["followers_count"]
		else:
			vTxD.append(numToday)
			vTxDp.append(ponToday)
			vD.append(str(actualMonth)+"-"+str(actualDay))
			numToday=1
			ponToday=tweet["user"]["followers_count"]
			actualDay=tweet["created_at"].tm_mday 
			actualMonth = tweet["created_at"].tm_mon
	
	vTxD.append(numToday)
	vTxDp.append(ponToday)
	vD.append(str(actualMonth)+"-"+str(actualDay))
	

	#dibuixem
	import numpy as np
	import matplotlib.pyplot as plt

	N = len(vD)
	ind = np.arange(N)  # the x locations for the groups
	width = 1.       # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, vTxD, width, color='r')

	# add some text for labels, title and axes ticks
	ax.set_ylabel('#Tweets')
	ax.set_title('Day')
	ax.set_xticks(ind+width/2)
	ax.set_xticklabels(vD,rotation='vertical')

	plt.savefig('plots/timeEvolution.png')
	
	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, vTxDp, width, color='r')

	# add some text for labels, title and axes ticks
	ax.set_ylabel('#TweetsPon')
	ax.set_title('Day')
	ax.set_xticks(ind+width/2)
	ax.set_xticklabels(vD,rotation='vertical')
	
	plt.savefig('plots/timeEvolutionPondered.png')


if __name__ == "__main__":
    main()
