import requests
import json
import os
from prettytable import PrettyTable

def authGen():
    username = os.environ["MTGUSER"]
    password = os.environ["MTGPASS"]
    authUrl = "https://www.echomtg.com/api/user/auth/"
    payload = {"email":username, "password":password}
    instantiate = requests.post(authUrl,payload)
    result = json.loads(instantiate.text)
    return result["token"]

def callWatchlist():
    start = 0
    end = 100
    inc = 100
    contents = []
    cont = True
    while cont:
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

def prettyWatchlist():
    rawData = callWatchlist()
    watchList = PrettyTable()
    watchList.field_names = ["name", "set", "tcg_low", "tcg_mid", "foil_price"]
    for i in rawData:
        watchList.add_row([i["name"], i["set"], i["tcg_low"], i["tcg_mid"], i["foil_price"]])
    watchList.align["name"] = "l"
    watchList.align["foil_price"] = "r"
    print watchList.get_string(sortby="foil_price")
        

def main():
    prettyWatchlist()

if __name__ == "__main__":
    main()
