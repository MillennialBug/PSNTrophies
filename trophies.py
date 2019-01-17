import bs4
import requests
#from models import trophies, db

USER = 'PhobiaB13'

res = requests.get('https://psnprofiles.com/' + USER + '/log')
soup = bs4.BeautifulSoup(res.text, 'html.parser')
maxpage = soup.select('#content > div > div > div.box.no-bottom-border > div > div > ul > li:nth-child(7) > a')

for y in range(1,int(maxpage[0].text.strip())):

    res = requests.get('https://psnprofiles.com/' + USER + '/log?dir=asc&page=' + str(y))
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

        print(trophyID[x].text.strip()[1:] + ' ' + gameTitle[x]['title'] + ' ' + trophyTitle[x].text.strip())

        '''row = trophies(Number = trophyID[x].text.strip()[1:],
                       Game   = gameTitle[x]['title'],
                       Name   = trophyTitle[x].text.strip(),
                       Text   = trophyText[x].text.strip()[len(trophyTitle[x].text.strip()):],
                       Date   = trophyDate[x].text.strip(),
                       Time   = trophyTime[x].text.strip(),
                       Rank   = trophyRank[x]['title'],
                       TrophyImage = trophyImage[x]['src'],
                       GameImage   = gameTitle[x]['src'])'''

        #db.session.add(row)
        #db.session.commit()
