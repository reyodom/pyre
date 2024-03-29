from datetime import datetime
import time
import pytz

def stiTime(ws, Channel):
    UTC = pytz.timezone('UTC')
    melb = pytz.timezone('Australia/Melbourne')
    stitime = datetime.utcnow().replace(tzinfo=UTC).astimezone(melb).strftime('It is %I:%M %p, on %d %B %Y in Melbourne, Australia.')
    ws("PRIVMSG {0} :{1}\r\n".format(Channel, stitime))
    