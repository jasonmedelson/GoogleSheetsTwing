from selenium import webdriver
from bs4 import BeautifulSoup
import gspread
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials
import time

#Google sheets linking
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope) #in same folder
client = gspread.authorize(creds)
sheet = client.open('daybreak twinge automation').sheet1

#stream names, must be exact
people = ["lirik","summit1g","drdisrespectlive","IzakOOO","sodapoppin","TimTheTatman","JoshOG","Ninja","Anthony_kongphan","gotaga","GoldGlove","Stormen","Nick28T","GassyMexican","sxyhxy","ErycTriceps","Trick2g","MoManus","iijeriichoii","CDNThe3rd","ANGRYPUG","Pineaqples","GrimmyBear","Symfuhny","FemSteph","Aydren","VernNotice","DrasseL","HOOWy","Emzia","prodigyacestv","Zeeth","ZombiUnicorn","p90princess","SoVindictive","julia_tv","NightwalkeR1H","CaLLzyy"]
browser = webdriver.Chrome() #exe file in sam folder
for number in range(0,len(people)): #loop through each streamer
    sheet.update_cell(number+2,1,people[number]) #add name to sheet
    url = "http://twinge.tv/channels/" + people[number] + '/'
    #print(url) #for keeping track of how far it has gone
    browser.get(url) #navigate to the page
    time.sleep(1) #allow js to load
    innerHTML = browser.page_source
    soup = BeautifulSoup(innerHTML, 'html.parser')
    follower = soup.find_all("div", { "class" : "channelStats__column--left" })
    followers1 = follower[0].text
    followers1 = followers1.split(" ")
    followers1 = followers1[0].strip()
    sheet.update_cell(number+2,2,followers1)#number of followers
    avg = soup.find_all("div", { "class" : "channelStats__column" })
    avg1 = avg[0].text
    avg1 = avg1.split(" ")
    avg1 = avg1[0].strip()
    sheet.update_cell(number+2,3,avg1)#Average number of viewers
    view = soup.find_all("div", { "class" : "channelStats__column--right" })
    view1 = view[0].text
    view1 = view1.split(" ")
    view1 = view1[0].strip()
    sheet.update_cell(number+2,4,view1)#Total views
    url = url + "games/#/30" # change number for different time span
    wait = 1
    while True:
        browser.get(url)
        time.sleep(wait) # allow js to load
        #innerHTML = browser.execute_script("return document.body.innerHTML")
        innerHTML = browser.page_source
        soup = BeautifulSoup(innerHTML, 'html.parser')
        games = soup.find_all("div", { "class" : "channelAllGames__meta" })
        games1 = games[0].text
        games1 = games1.split("\n")
        totaltime = games1[2].strip() #total time streamed
        check = totaltime.encode('ascii','ignore') #unicode to ascii
        totalgames = games1[6].strip() #total games
        totalgames = totalgames.encode('ascii','ignore') 
        wait = wait + 1
        if wait == 10: #if does not work by 10 something else is wrong
            break
        if totaltime != '0:00': # check to see if js has loaded
            break
    sheet.update_cell(number+2,5,totaltime)
    allgames = soup.find_all("td", { "class" : "ng-binding" })
    H=False # h1 found
    P=False # pubg found
    x = 0 #loop counter
    while (H == False or P == False) and x < int(totalgames):#loops through all games streamer has played
        if wait == 10:
            print("error occured") #notify error occured on streamer, break prevent error due to lack of data
            break
        game1 = allgames[x*3].text
        game1 = game1.split("\n")
        name1 = game1[1].strip()#game name, only care if h1z1 or pubg
        if name1 == "H1Z1: King of the Kill":
            H = True
            allgames1 = soup.find_all("td", { "class" : "channelAllGames__hover" })
            gamedata0 = allgames1[x].text
            gamedata0 = gamedata0.split("\n")
            h1time = (gamedata0[1].strip())#stream time as time
            h1per = (gamedata0[2].strip())#stream time as percentage
            h1views = (allgames[x*3+1].text)#name1 viewer%
            sheet.update_cell(number+2,9,h1time)
            sheet.update_cell(number+2,10,h1per)
            sheet.update_cell(number+2,11,h1views)
        elif name1 == "PLAYERUNKNOWN'S BATTLEGROUNDS":
            P = True
            allgames1 = soup.find_all("td", { "class" : "channelAllGames__hover" })
            gamedata0 = allgames1[x].text
            gamedata0 = gamedata0.split("\n")
            pubtime = (gamedata0[1].strip())#stream time as time
            pubper = (gamedata0[2].strip())#stream time as percentage
            pubviews = (allgames[x*3+1].text)#name1 viewer%
            sheet.update_cell(number+2,6,pubtime)
            sheet.update_cell(number+2,7,pubper)
            sheet.update_cell(number+2,8,pubviews)
        x=x+1
browser.quit()
