from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import datetime
import json

#Builds gets the database from Google Trends
def dataFrameCreator(keyWord,timeChecked): #timeframes: #-m, #-d, #-y, #-h
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = [keyWord]
    pytrends.build_payload(kw_list, cat=0, timeframe=timeChecked, geo='', gprop='')
    searchDataFrame=pytrends.interest_over_time()
    return searchDataFrame

#Outputs the average value of dataframe values.
def dataFrameCalculator(searchDataFrame):
    meanDataFrame=np.mean(searchDataFrame)
    lastDataDivided=searchDataFrame.div(meanDataFrame)
    return lastDataDivided

#check accuracy below.
def accuracyCheck(searchDataFrame,meanDataFrame,lastDataDivided,sizelastDataDivided):
    print(searchDataFrame)
    print(meanDataFrame)
    print(lastDataDivided)
    print(lastDataDivided.iat[sizelastDataDivided-1,0])

#Calculates the increase in search trends for each keyword within itself.
def makeMeRich(lastDataDivided):
    totalIncrease=0
    for x in range(sizelastDataDivided-5,sizelastDataDivided):
        if(lastDataDivided.iat[x,0]>2):
            totalIncrease+=1
    if(totalIncrease>1):
        isTwice=lastDataDivided.iat[sizelastDataDivided-1,0]/lastDataDivided.iat[sizelastDataDivided-2,0]
        print("\n"+keyWord+" için son data/önceki data oranı "+str(isTwice))
        if(isTwice>2):
            print("\n"+"Yırttık abicim "+keyWord+"'e bas evi.")
    print(keyWord+" "+str(totalIncrease)+" kere 2'den büyük çıktı.")

#Will be taking inputs after the user interface is set up.
def userPrompt():
    timeInputDate=input("1. Hour\n2. Day\n3. Month\n4. Year\n")
    timeInputDate=int(timeInputDate)
    if(timeInputDate==1):
        dayOrWeek="h"
        print("Hour")
    elif(timeInputDate==2):
        dayOrWeek="d"
        print("Day")
    elif(timeInputDate==3):
        dayOrWeek="m"
        print("Months")
    elif(timeInputDate==4):
        dayOrWeek="y"
        print("Years")
    else:
        print("You suck.")

    timeInputDay=input("How many "+dayOrWeek+"?\n")
    timeInputDay=int(timeInputDay)
    timeChecked=str('today '+str(timeInputDay)+'-'+str(dayOrWeek))

#Creates the config file
def createConfig():
    global coinList
    try:
        with open('trendsTrackerConfig.json','r') as reading:
            inputData=json.load(reading)
        coinList=inputData['key1']
        print("Config file has the following coins.\n")
        print(coinList,"\n")
    except:
        configCreate={"key1":["Input1","Input2","Input3"]}
        with open('trendsTrackerConfig.json','w') as configJson:
            json.dump(configCreate, configJson)
        print("Config file has been created. Please adjust the file before running the program.\n")
    return coinList


createConfig()


#Keywords to check
#checkKeywordList=["SRM","CHZ","SXP","PORT","SBR","AAVE","MINA","FTT","QRC","Strax","OGN","WAXP","ENJ","MANA"]
#checkKeywordList=["FTT"]   #Use this to check a single keyword.

#Gets the keywords to check from config file
checkKeywordList=coinList


timeChecked='today 3-m'

print("Searching for: "+timeChecked)

#Checks every keyword's trend within itself, seperately.
for i in checkKeywordList:
    keyWord=i
    searchDataFrame=dataFrameCreator(keyWord,timeChecked)
    meanDataFrame=np.mean(searchDataFrame)
    lastDataDivided=searchDataFrame.div(meanDataFrame)
    sizelastDataDivided=len(lastDataDivided)
    makeMeRich(lastDataDivided)

input("Press Enter")
#accuracyCheck(searchDataFrame, meanDataFrame, lastDataDivided, sizelastDataDivided)  #Check Accuracy for a keyword.
