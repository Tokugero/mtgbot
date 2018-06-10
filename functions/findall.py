import ebay
import mtgecho
import json
from prettytable import PrettyTable
import threading
import isodate

#This does the major work and stitches together the results


#    for i in results["findItemsByOKeywordsResponse"][0]["searchResult"][0]["item"]:
#        listings.add_row([i["title"][0][:25], i["sellingStatus"][0]["currentPrice"][0]["__value__"], isodate.parse_duration(i["sellingStatus"][0]["timeLeft"][0]), i["viewItemURL"][0]])
# {u'findItemsByKeywordsResponse': [{u'itemSearchURL': [u'http://www.ebay.com/sch/i.html?_nkw=Sol+Ring+Masterpiec&fscurrency=USD&_ddo=1&_ipg=100&_mPrRngCbx=1&_pgn=1&_sop=1&_udhi=5'], u'paginationOutput': [{u'totalPages': [u'0'], u'entriesPerPage': [u'100'], u'pageNumber': [u'0'], u'totalEntries': [u'0']}], u'ack': [u'Success'], u'timestamp': [u'2018-06-05T14:22:32.580Z'], u'searchResult': [{u'@count': u'0'}], u'version': [u'1.13.0']}]}
def searchEbay(card, cardList):
    #TODO: Build an actual class to define this, would probably be easier to read
    resultList = {}
    resultList["id"] = [card["watchlist_id"]]
    resultList["ebay"]={}
    resultList["ebay"]["results"] = []
    resultList["card"] = card
    allListings = []
    #Get the first word of the set of the card for query purposes
    cardSet = card["set"].split()[0]
    #The below functionality is to decipher: is it worth searching for foil, and is it worth searching for non foil. This is only if tcgplayer has prices stored at mtgecho
    if not cardSet:
        cardSet = str(card["set"])
    if card["foil_price"]:
        #The word "foil" is added to the query, may be ineligant... should talk to my ebros to get mtg metadata set :3
        foilResults = ebay.queryEbay(cardSet+" foil "+card["name"], card["foil_price"])
        if foilResults["findItemsByKeywordsResponse"][0]["paginationOutput"][0]["totalEntries"][0] !=  "0":
            for listing in foilResults["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]:
                #TODO Also need an actual class to define this object, would be easier and cleaner
                #Parse the information out into bite sized chunks for processing
                ebayObject = {}
                ebayObject["type"]="Foil"
                ebayObject["name"] = listing["title"][0]
                ebayObject["tte"] = isodate.parse_duration(listing["sellingStatus"][0]["timeLeft"][0])
                ebayObject["url"] = listing["viewItemURL"][0]
                ebayObject["price"] = listing["sellingStatus"][0]["currentPrice"][0]["__value__"]
                allListings.append(ebayObject)
            #Add result to a list for future returns (this is going to be an async call after all)
            resultList["ebay"]["results"].append(allListings)
    if card["tcg_low"]:
        nonFoilResults = ebay.queryEbay(cardSet+" "+card["name"], card["tcg_low"])
        if nonFoilResults["findItemsByKeywordsResponse"][0]["paginationOutput"][0]["totalEntries"][0] != "0":
            for listing in nonFoilResults["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]:
                ebayObject = {}
                ebayObject["type"]="Non-Foil"
                ebayObject["name"] = listing["title"][0]
                ebayObject["tte"] = isodate.parse_duration(listing["sellingStatus"][0]["timeLeft"][0])
                ebayObject["url"] = listing["viewItemURL"][0]
                ebayObject["price"] = listing["sellingStatus"][0]["currentPrice"][0]["__value__"]
                allListings.append(ebayObject)
            resultList["ebay"]["results"].append(allListings)
    #Add result list dict to a global array so this can be made asynchroonously
    cardList.append(resultList)

#Thread these calls or it'll take forever
def findEbayWatchlist():
    #Single call, get watchlist
    watchList = mtgecho.callWatchlist()
    threads = []
    cardList = []
    #For each card, define a thread to call
    for card in watchList:
        functionThread = threading.Thread(target=searchEbay, args=(card,cardList,))
        threads.append(functionThread)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return cardList 

#This is just to pretty output this to CLI, it could just as easily be made to define the objects and pass them around somewhere else.. dirty dirty data.
def cliOutput():
    result = findEbayWatchlist()
    mt = PrettyTable()
    mt.field_names = ["Card Name", "TCG Low", "Foil Mid", "eBay Listings"]
    for row in result:
        st = PrettyTable()
        st.field_names = ["Ending", "Price", "Foil?", "URL"]
        if row["ebay"]["results"]:
            for results in row["ebay"]["results"]:
                for listing in results:
                    st.add_row([listing["tte"], listing["price"], listing["type"], listing["url"]])
        st.align["URL"] = "l"
        st.align["Price"] = "r"
        st.sortby = "Ending"
        mt.add_row([row["card"]["set_code"]+" - "+row["card"]["name"], row["card"]["tcg_low"], row["card"]["foil_price"], st])
    mt.align["eBay Listings"] = "l"
    mt.align["Card Name"] = "l"
    mt.align["TCG Low"] = "r"
    mt.align["Foil Mid"] = "r"
    print mt

def main():
    print cliOutput()

if __name__ == "__main__":
    main()
