from dns import resolver,reversename
from re import search

gtlds = ['aero', 'asia', 'biz', 'cat', 'com', 'coop', 'edu', 'gov', 'info',
'int', 'jobs', 'mil', 'mobi', 'museum', 'name', 'net', 'org', 'pro', 'tel',
'travel', 'xxx', ]

cctlds = ['ac', 'ad', 'af', 'ag', 'ai', 'al', 'am', 'an', 'ao', 'aq', 'ar',
'as', 'at', 'au', 'aw', 'ax', 'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg',
'bh', 'bi', 'bj', 'bm', 'bn', 'bo', 'br', 'bs', 'bt', 'bv', 'bw', 'by',
'bz', 'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn',
'co', 'cr', 'cs', 'cu', 'cv', 'cx', 'cy', 'cz', 'de', 'dk', 'ec', 'ee',
'eg', 'es', 'eu', 'fi', 'fr', 'gb', 'gr', 'hk', 'hr', 'id', 'ie', 'il',
'iq', 'ir', 'is', 'it', 'jm', 'jp', 'kg', 'kp', 'kr', 'kw', 'kz', 'la',
'lb', 'li', 'lc', 'lt', 'lu', 'lv', 'ly', 'me', 'mk', 'mo', 'mv', 'mx',
'my', 'na', 'nc', 'ne', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz',
'om', 'pa', 'ph', 'pk', 'pl', 'pt', 'qa', 're', 'ro', 'rs', 'ru', 'sa',
'sd', 'se', 'sg', 'sh', 'sk', 'sl', 'sj', 'so', 'ss', 'su', 'sv', 'sy',
'tc', 'td', 'th', 'tk', 'tl', 'tm', 'tn', 'to', 'tr', 'tt', 'tv', 'tw',
'tz', 'ua', 'ug', 'uk', 'us', 'uy', 'va', 'vc', 've', 'vg', 'vi', 'vn',
'vu', 'ws', 'ye', 'yt', 'za']

rDNSWhitelist = ['stal', 'Thorn', 'Faust', 'Ferus']

def rLookup(addr):
    try:
        r = resolver.query(reversename.from_address(addr),"PTR")[0]
        return '{0} resolves to \'{1}\'\r\n'.format(addr, str(r))
    except:
        return 'rDNS lookup failed for {0}\r\n'.format(addr)
def dLookup(addr):
    try:
        r = resolver.query(addr)[0]
        return '{0} resolves to \'{1}\'\r\n'.format(addr, str(r))
    except:
        return 'DNS lookup failed for {0}\r\n'.format(addr)

def detect(ws, Nick, Channel, addr):
    addr = addr.lstrip('http://')
    addr = addr.partition('/')[0]
    if search('^([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])$', addr):
        if Nick in rDNSWhitelist:
            ws('PRIVMSG {0} :{1}\r\n'.format(Channel, rLookup(addr)))
        else:
            ws('PRIVMSG {0} :No reverse lookups for you.\r\n'.format(Channel))
    else:
        d = addr.split('.')
        if (d[len(d) - 1] in gtlds) or (d[len(d) - 1] in cctlds):
            ws('PRIVMSG {0} :{1}\r\n'.format(Channel, dLookup(addr)))
        else:
            ws('PRIVMSG {0} :\'{1}\' is not a valid TLD!\r\n'.format(Channel, d[len(d) - 1]))

