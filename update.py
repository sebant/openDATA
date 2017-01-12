#busquem nous tweets
import request
request.main()

#ajuntem totes les busquedes i generem fitxes mes manejables en "tables/"
import generateTable
generateTable.main()

#analisis del nombre de tweets en funcio del temps, i de la propagacio de tweets en funcio del temps
import timeAnalisis
timeAnalisis.main()

#busquem totes els seguidors de cada twitaire
import requestFollowers
requestFollowers.main()