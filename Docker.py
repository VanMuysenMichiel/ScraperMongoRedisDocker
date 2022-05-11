import requests
from bs4 import BeautifulSoup as BS
import pymongo as mongo
import redis


goat = 0
time= ""
list = []
keepGoing = True

client = mongo.MongoClient("mongodb://localhost:27777")
mydb = client["Scraper"]
mycol = mydb["Data"]

r = redis.Redis(port= 6555,charset="utf-8", decode_responses=True)

while keepGoing == True:
    
    request = requests.get("https://www.blockchain.com/btc/unconfirmed-transactions")
    only_text = request.text
    soup = BS(only_text, "html.parser")
    data = soup.find_all("div", {"class" : "sc-1g6z4xm-0 hXyplo"})

    for d in data:
        text = d.text
        text = text.replace("Hash","")
        text = text.replace("Time"," ")
        text = text.replace("Amount","")
        text = text.replace("(BTC)","")
        text = text.replace("BTC","")
        text = text.replace(" (USD)","")
        text = text.split(" ")
        list.append(text)

    list.reverse()

    if len(time) == 0:
            time = text[1]

    for index in list:

        if index[1] == time:
 
            n0 = str(index[0])
            n1 = str(index[1])
            n2 = str(index[2])
            n3 = str(index[3])
            
            listOfStrings = [n0,n1,n2,n3]
            finalString = " ".join(listOfStrings)

            r.lpush("Data",finalString)

            if float(index[2]) > goat:

                goat = float(index[2])

                highest = index[0]
                timeHighest = index[1]
                BTC = index[2]
                USD = index[3]

        if index[1] > time: 

            mydict = {"Hash": highest, "Time": timeHighest, "BTC": str(BTC) + " BTC", "USD": USD}

            y = mycol.insert_one(mydict)

            r.persist("Data")
            time = index[1]
            goat = 0 
            list = [] 

            y.inserted_id   