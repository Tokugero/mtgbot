import ebay
import mtgecho
import json
from prettytable import PrettyTable
import threading
import isodate

#    for i in results["findItemsByOKeywordsResponse"][0]["searchResult"][0]["item"]:
#        listings.add_row([i["title"][0][:25], i["sellingStatus"][0]["currentPrice"][0]["__value__"], isodate.parse_duration(i["sellingStatus"][0]["timeLeft"][0]), i["viewItemURL"][0]])
def searchEbay(card, cardList):
    resultList = {}
    resultList["id"] = [card["watchlist_id"]]
    resultList["ebay"]={}
    resultList["card"] = card
    allListings = []
    cardSet = card["set"].split()[0]
    if not cardSet:
        cardSet = str(card["set"])
    if card["foil_price"]:
        foilResults = ebay.queryEbay(cardSet+" foil "+card["name"], card["foil_price"])
        #PLACEMARKER - Working on building out an object to store the foil results and non-foil results as a [cardObject:[ebaylistings],...]
        ebay = {}
        ebay["type"]="Foil"
        for listing in foilResults["findItemsByKeywordsResponse"][0]["searchResult"][0]:
            ebay["name"] = listing["title"]
            ebay["tte"] = isodate.parse_duration(i["timeleft"][0])
            allListings.append(ebay)
        resultList["ebay"]["foilResults"] = allListings
    if card["tcg_low"]:
        ebay["type"]="Non-Foil"
        nonFoilResults = ebay.queryEbay(cardSet+" "+card["name"], card["tcg_low"])
        for listing in nonFoilResults["findItemsByKeywordsResponse"][0]["searchResult"][0]:

        resultList["ebay"]["nonFoilResults"] = nonFoilResults
    cardList.append(resultList)

def findEbayWatchlist():
    watchList = mtgecho.callWatchlist()
    threads = []
    cardList = []
    for card in watchList:
        functionThread = threading.Thread(target=searchEbay, args=(card,cardList,))
        threads.append(functionThread)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    for card in cardList:
        print card["card"]["name"] 
    return cardList 

def main():
    result = findEbayWatchlist()

if __name__ == "__main__":
    main()
