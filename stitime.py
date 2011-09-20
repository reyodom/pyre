from datetime import datetime
import time
import pytz

def stiTime():
    UTC = pytz.timezone('UTC')
    melb = pytz.timezone('Australia/Melbourne')
    stitime = str(datetime.utcnow().replace(tzinfo=UTC).astimezone(melb)).split('+')[0]
    return '\x02STITime\x02: {0}'.format(stitime.split('.')[0])
    