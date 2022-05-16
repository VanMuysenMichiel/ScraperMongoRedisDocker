#Packages
import requests
from bs4 import BeautifulSoup as BS
import pymongo as mongo
import redis

#MongoDB
client = mongo.MongoClient("mongodb://localhost:27777") #27017
mydb = client["Scraper"]
mycol = mydb["Data"]

#Redis
r = redis.Redis(port= 6555,charset="utf-8", decode_responses=True) #6379

goat = 0
time= ""
scrapedData = []
keepGoing = True

#Keep it running all the time
while keepGoing == True:
    
    #Scraper itself
    request = requests.get("https://www.blockchain.com/btc/unconfirmed-transactions")
    only_text = request.text
    soup = BS(only_text, "html.parser")
    data = soup.find_all("div", {"class" : "sc-1g6z4xm-0 hXyplo"})

    #Data cleaning
    for d in data:
        text = d.text
        text = text.replace("Hash","")
        text = text.replace("Time"," ")
        text = text.replace("Amount","")
        text = text.replace("(BTC)","")
        text = text.replace("BTC","")
        text = text.replace(" (USD)","")
        text = text.split(" ")
        scrapedData.append(text)

    #Reverse the list --> so the newest data gets in the front
    scrapedData.reverse()

    #Take the first date as start
    if len(time) == 0:
            time = text[1]

    #Loop the scraped data
    for index in scrapedData:

        #Do this when the newest data is the same as the previous one
        if index[1] == time:
 
            #My way to push al the data to Redis and use it as a caching mechanism
            n0 = str(index[0])
            n1 = str(index[1])
            n2 = str(index[2])
            n3 = str(index[3])
            
            listOfStrings = [n0,n1,n2,n3]
            finalString = " ".join(listOfStrings)

            r.lpush("Data",finalString)

            #To see which hash is the biggest
            if float(index[2]) > goat:

                goat = float(index[2])

                highest = index[0]
                timeHighest = index[1]
                BTC = index[2]
                USD = index[3]

        # Do this when the time has changed in the scraped data
        if index[1] > time: 

            #Send the biggest hash of the minute to MongoDB
            mydict = {"Hash": highest, "Time": timeHighest, "BTC": str(BTC) + " BTC", "USD": USD}

            y = mycol.insert_one(mydict)

            #Delete evey variable, so we can begin the process again
            r.persist("Data")
            time = index[1]
            goat = 0 
            scrapedData = [] 

            y.inserted_id   