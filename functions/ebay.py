import requests
import json
import os
from prettytable import PrettyTable

def queryEbay(query):
    appid = os.environ["EBAYAPPID"]
    url = "https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords"
    instantiate = requests.get(url+"&SERVICE-VERSION=1.0.0&SECURITY-APPNAME="+appid+"&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords="+query)
    response = json.loads(instantiate.text)
    return response

def cliReturn(query):
    results = queryEbay(query)
    listings = PrettyTable()
    listings.field_names = ["Title", "Price", "Time Left", "Buy it Now?", "Listing End Time", "URL"]
    for i in results["findItemsByKeywordsResponse"]:
        print i
        listings.add_row([i["title"], i["sellingStatus"]["currentPrice"], i["timeLeft"], i["buyItNowAvailable"], i["endTime"], i["viewItemURL"]])
    print listings

def main():
    print cliReturn("Magic the Gathering")

if __name__ == "__main__":
    main()
