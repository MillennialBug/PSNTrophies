from models import trophies, db
import re
from datetime import datetime


def format_datetime(date, time):
    dt = datetime.strptime(re.sub(r'th|nd|st|rd|\s', '', date).zfill(9), '%d%b%Y')
    time = re.sub(r'\sAM|\sPM', '', time).zfill(8)
    return f'{dt.strftime("%Y-%m-%d")} {time}'


if __name__ == "__main__":
    rows = db.session.query(trophies).all()

    for row in rows:
        print(f'{row.User} {row.Number}')
        row.DateTime = format_datetime(row.Date, row.Time)

    db.session.commit()
