# botCore.
# This manages Lyra's connection to IRC.
# v1.6, by stal

import socket
import time
import string
from botparse import Admin
import config

Admin = Admin()
s=socket.socket( )
OurNick = '?'
connected = 0

def connect():
    Admin.Load()
    print '--- {0} Opening connection to {1} on port {2}'.format(config.tagI, config.Host, config.Port)
    s.connect((config.Host, config.Port))
    connected=1
    print '--- {0} Registering with IRCd using nick {1}, ident {2} and realname {3}'.format(config.tagI, config.Nick, config.Ident, config.RealName)
    register(config.Nick)
    
def writeSock(data):
    time.sleep(0.5)
    print '>>> {0}'.format(string.rstrip(data))
    s.send(data)
    
def quitIRC(msg):
    s.send("QUIT {0}\r\n".format(msg))
    s.close()
    
def register(n):
    s.send("NICK {0}\r\n".format(n))
    s.send("USER {0} {1} dildos :{2}\r\n".format(config.Ident, config.Host, config.RealName))
    
def connectCmds():
    print '--- {0} Running connect commands'.format(config.tagI)
    s.send("MODE {0} +B\r\n".format(OurNick))
    if OurNick == 'Lyra' or OurNick == 'Mami':
        s.send("PRIVMSG {0} :IDENTIFY {1}\r\n".format(config.NickService, config.NickPass))
    time.sleep(2)
    s.send("JOIN {0}\r\n".format(config.Channels))
    