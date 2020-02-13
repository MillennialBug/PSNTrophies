import inkyphat
from PIL import ImageFont, Image
from sqlalchemy.sql.expression import func
from models import trophies, db
from bs4 import BeautifulSoup
from requests import get
from datetime import datetime

updated = 'updated: ' + datetime.now().strftime('%d/%m/%y %H:%M')
PSNPROFILES = 'https://psnprofiles.com/'
user = 'MillennialBug'
bronze = 'Bronze'
silver = 'Silver'
gold = 'Gold'
platinum = 'Platinum'

inkyphat.clear()
inkyphat.set_colour("black")
p_font = ImageFont.truetype(inkyphat.fonts.FredokaOne, 19)
g_font = ImageFont.truetype(inkyphat.fonts.FredokaOne, 15)
s_font = ImageFont.truetype(inkyphat.fonts.FredokaOne, 12)
b_font = ImageFont.truetype(inkyphat.fonts.FredokaOne, 9)
u_font = ImageFont.truetype(inkyphat.fonts.FredokaOne, 8)

res = get(PSNPROFILES + user + '/log?page=0')
res.raise_for_status()
soup = BeautifulSoup(res.text, 'html.parser')
level = soup.select('.trophy-count > ul > li')
level = level[0].text.strip()

bronze_count = db.session.query(func.count(trophies.Number)). \
        filter(trophies.Rank == bronze).scalar()
silver_count = db.session.query(func.count(trophies.Number)). \
        filter(trophies.Rank == silver).scalar()
gold_count = db.session.query(func.count(trophies.Number)). \
        filter(trophies.Rank == gold).scalar()
plat_count = db.session.query(func.count(trophies.Number)). \
        filter(trophies.Rank == platinum).scalar()

inkyphat.set_image(Image.open("trophies-bw.png"))
inkyphat.text((23,43), str(plat_count), inkyphat.BLACK, p_font)
inkyphat.text((72,64), str(gold_count), inkyphat.BLACK, g_font)
inkyphat.text((124,76), str(silver_count), inkyphat.BLACK, s_font)
inkyphat.text((169,90), str(bronze_count), inkyphat.BLACK, b_font)
inkyphat.text((1,95), updated, inkyphat.BLACK, u_font)
inkyphat.text((124,1), user, inkyphat.WHITE, s_font)
inkyphat.text((172,29), str(level), inkyphat.WHITE, s_font)

inkyphat.show()
