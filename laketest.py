import lakepy as lk
# for scraping
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
# for data
import pandas as pd
import re

def main():
    page = requests.get("https://mead.uslakes.info/level/")
    if page.status_code == 200:
        print( "Open Success!")
        # print( page.content)
        content = page.content
        soup = BeautifulSoup( content, 'html.parser')
    else:
        print( "Error opening webpage")
        exit(1)

    # print( soup.prettify())
    # html = list( soup.children)[3]
    # print( list( html.children))
    # water_level = soup.find( id="WATER LEVEL")

    main = list( soup.find(id="main-content"))
    box = main[5]
    text = box.get_text()
    lines = text.split("\n")
    parsed = list(filter(lambda a: a != '', lines))

    data = {}
    data["water_level"] = parsed[1]
    data["date"] = parsed[3]
    data["time"] = parsed[4][3:]
    data["below"] = re.findall( r'\d+.\d+', parsed[5])[0]
    data["full_pool"] = re.findall( r'\d+.\d+', parsed[9])[0]
    data["change"] = re.findall( r'\d+.\d+', parsed[11])[0]

    tweet_text = "As of %s, %s Pacific Time, the water level at Lake Mead is at %s ft, which is %s ft below the full pool of %s ft\n\n"%( data["time"], data["date"], data["water_level"], data["below"], data["full_pool"])
    tweet_text = tweet_text + "This is a %s foot change from yesterday"%(data["change"])
    alt_tweet_text = altText( data)
    print( tweet_text)
    print( alt_tweet_text)
    print("done :)")

def altText( data):
    text = "Date and Time: %s %s \n"%( data["time"], data["date"])
    text = text + "Water Level: %s feet \n"%( data["water_level"])
    text = text + "Below Pool: %s feet \n"%( data["below"])
    text = text + "Daily Change: %s feet \n"%( data["change"])
    return text
    
def HistoricalData():
    mead = lk.search( id_No = 237)
    print( mead.observation_period)
    print( mead.data)

if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        
