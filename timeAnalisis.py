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
	vD=[]
	actualDay = slTweets[0]["created_at"].tm_mday
	numToday = 0
	for tweet in slTweets:
		if tweet["created_at"].tm_mday == actualDay:
			numToday=numToday+1
		else:
			vTxD.append(numToday)
			vD.append(actualDay)
			numToday=1
			actualDay=tweet["created_at"].tm_mday 


	#dibuixem
	import numpy as np
	import matplotlib.pyplot as plt

	N = len(vD)
	
	ind = np.arange(N)  # the x locations for the groups
	width = 0.35       # the width of the bars

	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, vTxD, width, color='r')

	# add some text for labels, title and axes ticks
	ax.set_ylabel('#Tweets')
	ax.set_title('Day')
	ax.set_xticks(ind + width)
	ax.set_xticklabels(vD)

	
	plt.savefig('plots/foo.png')



if __name__ == "__main__":
    main()
