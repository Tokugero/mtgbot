import requests
import json
import os
from prettytable import PrettyTable
import isodate

def queryEbay(query, maxPrice):
    appid = os.environ["EBAYAPPID"]
    url = "https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords"
    instantiate = requests.get(url+"&SERVICE-VERSION=1.0.0&SECURITY-APPNAME="+appid+"&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&sortOrder=EndTimeSoonest&itemFilter.name=MaxPrice&itemFilter.value="+str(maxPrice)+"&keywords="+query)
    response = json.loads(instantiate.text)
    return response

def cliReturn(query, maxPrice):
    results = queryEbay(query, maxPrice)
    listings = PrettyTable()
    listings.field_names = ["Title", "Price", "Time Left", "URL"]
    for i in results["findItemsByKeywordsResponse"][0]["searchResult"][0]["item"]:
        listings.add_row([i["title"][0][:25], i["sellingStatus"][0]["currentPrice"][0]["__value__"], isodate.parse_duration(i["sellingStatus"][0]["timeLeft"][0]), i["viewItemURL"][0]])
    listings.align["URL"] = "l"
    listings.align["Title"] = "l"
    print listings

def main():
    print cliReturn("Sol Ring Masterpiec", 500)

if __name__ == "__main__":
    main()
