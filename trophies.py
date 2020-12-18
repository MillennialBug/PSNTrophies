from bs4 import BeautifulSoup
from requests import get
from models import trophies, db
import re
from sqlalchemy.sql.expression import func
import os.path
from datetime import datetime
from sys import platform

PSNPROFILES = 'https://psnprofiles.com/'
users = ('MillennialBug', 'Coggins3842', 'WorldWildeWest')
PATH = {'linux': '/home/pi/',
        'win32': 'c:/users/pj-wr/'}


def format_datetime(date, time):
    dt = datetime.strptime(re.sub(r'th|nd|st|rd|\s', '', date).zfill(9), '%d%b%Y')
    time = re.sub(r'\sAM|\sPM', '', time).zfill(8)
    return f'{dt.strftime("%Y-%m-%d")} {time}'


for user in users:
    maxTrophy = db.session.query(func.max(trophies.Number)).filter(trophies.User == user).scalar()
    if maxTrophy is None:
        maxTrophy = 0

    res = get(PSNPROFILES + user + '/log')
    soup = BeautifulSoup(res.text, 'html.parser')
    maxpage = soup.select('#content > div > div > div.box.no-bottom-border > div > div > ul > li:nth-child(7) > a')

    for y in range(1, int(maxpage[0].text.strip()) + 1):

        res = get(PSNPROFILES + user + '/log?page=' + str(y))
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        trophiesOnPage = soup.select('.zebra > tr')
        count = len(trophiesOnPage)
        trophyID = soup.select('.zebra > tr > td:nth-child(5)')

        if int(re.sub(',', '', trophyID[0].text.strip()[1:])) <= maxTrophy:
            break

        gameTitle = soup.select('.zebra > tr > td > a > .game')
        trophyTitle = soup.select('.zebra > tr > td:nth-child(3) > a')
        trophyImage = soup.select('.zebra > tr > td:nth-child(2) > a > .trophy')
        trophyText = soup.select('.zebra > tr > td:nth-child(3)')
        trophyDate = soup.select('.zebra > tr > td:nth-child(6) > span > .typo-top-date')
        trophyTime = soup.select('.zebra > tr > td:nth-child(6) > span > .typo-bottom-date')
        trophyRank = soup.select('.zebra > tr > td:nth-child(10) > span > img')

        for x in range(0, count):

            if int(re.sub(',', '', trophyID[x].text.strip()[1:])) <= maxTrophy:
                break

            # print(trophyID[x].text.strip()[1:] + ' ' + gameTitle[x]['title'] + ' ' + trophyTitle[x].text.strip())

            hexCode = re.search(r'^https://i.psnprofiles.com/games/(.*)/trophies.*$', trophyImage[x]['src'])
            trophyImageFilename = re.split(r'/', trophyImage[x]['src'])

            if not os.path.exists(PATH[platform] + 'PSNTrophies/trophies/' + trophyImageFilename[6]):
                dl = get(trophyImage[x]['src'])
                if dl.status_code == 200:
                    with open(PATH[platform] + 'PSNTrophies/trophies/' + trophyImageFilename[6], 'wb') as timg:
                        for chunk in dl.iter_content(200000):
                            timg.write(chunk)
                    timg.close()

            gameImageFilename = re.split(r'/', gameTitle[x]['src'])
            if not os.path.exists(PATH[platform] + 'PSNTrophies/games/' + gameImageFilename[5]):
                dl = get(gameTitle[x]['src'])
                if dl.status_code == 200:
                    with open(PATH[platform] + 'PSNTrophies/games/' + gameImageFilename[5], 'wb') as timg:
                        for chunk in dl.iter_content(200000):
                            timg.write(chunk)
                    timg.close()

            row = trophies(Number=re.sub(',', '', trophyID[x].text.strip()[1:]),
                           Game=gameTitle[x]['title'],
                           Name=trophyTitle[x].text.strip(),
                           Text=trophyText[x].text.strip()[len(trophyTitle[x].text.strip()):],
                           Date=trophyDate[x].text.strip(),
                           Time=trophyTime[x].text.strip(),
                           DateTime=format_datetime(trophyDate[x].text.strip(), trophyTime[x].text.strip()),
                           Rank=trophyRank[x]['title'],
                           GameHex=hexCode.group(1),
                           TrophyImage=trophyImage[x]['src'],
                           GameImage=gameTitle[x]['src'],
                           User=user)

            db.session.add(row)

db.session.commit()
