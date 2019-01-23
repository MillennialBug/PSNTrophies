import bs4
import requests
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from models import trophies, db

def updateProfile(userid):
    
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(chrome_options=options)
    
    try:
        browser.get(PSNPROFILES)
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID,'psnId')))
    except TimeoutException as ex:
        print('Timeout while trying to load ' + PSNPROFILES)
        browser.quit()
        print('Quitting...')
        exit()

    psnId = browser.find_element(by=By.ID, value="psnId")
    psnId.send_keys(userid)
    psnId.send_keys(Keys.RETURN)
    
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#processing > #update > #update > center')))
        elem = browser.find_element(by=By.CSS_SELECTOR, value="#processing > #update > #update > center")
        print(userid + ' added to the queue.')
        sleep(1)
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#processing > #update > #update > center')))
        elem = browser.find_element(by=By.CSS_SELECTOR, value="#processing > #update > #update > center")
    except TimeoutException as ex:
        print('Timeout while attempting to update user "' + userid + '"')
        print('Quitting...')
        exit()
    finally:
        browser.quit()
        return elem

def updateSuccess(elem):
    if('has been updated' in elem.text):
        print(user + ' has been updated')
        return 'success'
    else if('PSNID could not be found' in elem.text):
        print(user + ' is not a valid PSN ID.')
        while(user2 == user):
            user2 = input("Please re-enter your PSN ID.\n")
            if(user2 == user):
                print('You have entered the same ID, please try again\n')
        user = user2
        return 'invalid'

PSNPROFILES = 'https://psnprofiles.com/'

'''
if(len(sys.argv) > 1):
    user = sys.argv[1]
else:
    user = input("Please enter your PSN ID.\n")'''

user = ''






result = updateProfile(user)
while(result != 'invalid'):
    result = updateProfile(user)
    






    
    
res = requests.get(PSNPROFILES + user + '/log')
soup = bs4.BeautifulSoup(res.text, 'html.parser')
maxpage = soup.select('#content > div > div > div.box.no-bottom-border > div > div > ul > li:nth-child(7) > a')

for y in range(1,int(maxpage[0].text.strip())):

    res = requests.get(PSNPROFILES + user + '/log?dir=asc&page=' + str(y))
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    trophiesOnPage = soup.select('.zebra > tr')
    count = len(trophiesOnPage)

    for x in range(0,count):

        gameTitle   = soup.select('.zebra > tr > td > a > .game')
        trophyTitle = soup.select('.zebra > tr > td:nth-child(3) > a')
        trophyImage = soup.select('.zebra > tr > td:nth-child(2) > a > .trophy')
        trophyText  = soup.select('.zebra > tr > td:nth-child(3)')
        trophyID    = soup.select('.zebra > tr > td:nth-child(5)')
        trophyDate  = soup.select('.zebra > tr > td:nth-child(6) > span > .typo-top-date')
        trophyTime  = soup.select('.zebra > tr > td:nth-child(6) > span > .typo-bottom-date')
        trophyRank  = soup.select('.zebra > tr > td:nth-child(10) > span > img')
        

        #print(trophyID[x].text.strip()[1:] + ' ' + gameTitle[x]['title'] + ' ' + trophyTitle[x].text.strip())

        row = trophies(Number = trophyID[x].text.strip()[1:],
                       Game   = gameTitle[x]['title'],
                       Name   = trophyTitle[x].text.strip(),
                       Text   = trophyText[x].text.strip()[len(trophyTitle[x].text.strip()):],
                       Date   = trophyDate[x].text.strip(),
                       Time   = trophyTime[x].text.strip(),
                       Rank   = trophyRank[x]['title'],
                       TrophyImage = trophyImage[x]['src'],
                       GameImage   = gameTitle[x]['src'])

        #db.session.add(row)
        #db.session.commit()
