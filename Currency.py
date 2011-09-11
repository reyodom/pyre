# Steal Google's API to convert currency.

import requests
import string
import botCore
import re
from decimal import Decimal, ROUND_HALF_UP

def currencyConvert(nick, chan, camount, cfrom, cto):
    try:
        Decimal(camount)
    except:
        botCore.writeSock('PRIVMSG {0} :That\'s not correct syntax.\r\n'.format(chan))
        return "bad"
    r = requests.get('http://google.com/ig/calculator?hl=en&q={0}{1}=?{2}'.format(camount, cfrom, cto))
    s=re.sub('[^A-Za-z0-9 \. \,\"]+', '', r.content)
    s=s.split('"')
    if s[5] == '4' or s[5] == 'Parse error in query.':
        botCore.writeSock('PRIVMSG {0} :That\'s not correct syntax.\r\n'.format(chan))
        return "bad"
    resultFrom = s[1].split(' ')
    resultTo = s[3].split(' ')
    roundedAmount = Decimal(resultTo[0]).quantize(Decimal("1") / (Decimal('10') ** 2), ROUND_HALF_UP) 
    botCore.writeSock('PRIVMSG {0} :{1}, {2} = {3} {4} {5}.\r\n'.format(chan, nick, string.join(resultFrom), roundedAmount, resultTo[1], resultTo[2]))
    return 'OK'
