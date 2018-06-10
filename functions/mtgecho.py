import requests
import json
import os
from prettytable import PrettyTable

#Make an auth call to get a token. It expires super fast, so it has to be made with each call.
def authGen():
    username = os.environ["MTGUSER"]
    password = os.environ["MTGPASS"]
    authUrl = "https://www.echomtg.com/api/user/auth/"
    payload = {"email":username, "password":password}
    instantiate = requests.post(authUrl,payload)
    result = json.loads(instantiate.text)
    return result["token"]

#Get the watchlist, paginates 100 items per request if needed
def callWatchlist():
    start = 0
    end = 100
    inc = 100
    contents = []
    cont = True
    while cont:
        #Generates new auth with each request
        token = authGen()
        watchUrl = "https://www.echomtg.com/api/watchlist/view/start="+str(start)+"&limit="+str(end)+"&auth="+token
        instantiate = requests.get(watchUrl)
        result = json.loads(instantiate.text)
        for i in result["items"]:
            contents.append(i)
        if len(contents) == end:
            start = end+1
            end = end+inc
        else:
            cont = False
    return contents

#This is just for sample output, not actually used elsewhere
def prettyWatchlist():
    rawData = callWatchlist()
    watchList = PrettyTable()
    watchList.field_names = ["name", "set", "tcg_low", "tcg_mid", "foil_price"]
    for i in rawData:
        watchList.add_row([i["name"], i["set"], i["tcg_low"], i["tcg_mid"], i["foil_price"]])
    watchList.align["name"] = "l"
    watchList.align["foil_price"] = "r"
    print watchList.get_string(sortby="foil_price")
        

#Sample output if you wanted to call this method on its lonesome, just a sample of how to call
def main():
    prettyWatchlist()

if __name__ == "__main__":
    main()
