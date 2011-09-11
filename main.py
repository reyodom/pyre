#!/usr/bin/env python
# ^ been meaning to put that there for weeks now
import botCore
import botparse
import string
import sys
import time
import config

class __init__():
    readbuffer = ""
    Admin = botparse.Admin()
    Utils = botparse.Utils()
    Parser = botparse.Parser()
    
    botCore.connect()
    connected = 1

    try:
        while connected == 1:
            readbuffer=readbuffer+botCore.s.recv(1024)
            t=string.split(readbuffer, "\n")
            readbuffer=t.pop( )
            for line in t:
                line=string.split(string.rstrip(line))
                if line[0] == 'PING' \
                or '00' in line[1] \
                or '25' in line[1] \
                or '26' in line[1] \
                or '37' in line[1] \
                or '433' in line[1]:
                    pass
                elif line[1] == 'NOTICE' and line[2] == 'AUTH':
                    pass
                else:    
                    print string.join(line)
                # these are more important, so use main to take care of them instead of botparse
                if(line[1]=="433"):
                    print '--- {0} Nick {1} is already taken!'.format(config.tagW, line[3])
                    botCore.OurNick = config.AltNick
                    botCore.register(config.AltNick)
                elif(line[1]=="001"):
                    print '--- {0} Successfully registered with IRCd.'.format(config.tagI)
                    botCore.OurNick = config.Nick
                    botCore.connectCmds()
                elif(line[0]=="PING"):
                    botCore.s.send("PONG {0}\r\n".format(line[1]))
                    print '--- {0} PONGed server. ({1})'.format(config.tagI, line[1].strip(':'))
                elif(line[1] == "PRIVMSG" and Utils.isChannel(line[2]) and line[3] == ":*rb"):
                    if Admin.Check(Utils.getHost(line[0])):
                        print '--- {0} Reloading botparse.'.format(config.tagW)
                        botCore.writeSock("PRIVMSG {0} :Okay, reloading botparse.\r\n".format(line[2]))
                        reload(botparse)
                        Admin = botparse.Admin()
                        Utils = botparse.Utils()
                        Parser = botparse.Parser()
                    else:
                        botCore.writeSock("PRIVMSG {0} :Permission denied.\r\n".format(line[2]))
                elif(line[1] == "PRIVMSG" and Utils.isChannel(line[2]) and line[3] == ":*debug"):
                    if Admin.Check(Utils.getHost(line[0])):
                        print readbuffer
                    else:
                        botCore.writeSock("PRIVMSG {0} :Permission denied.\r\n".format(line[2]))
                # pass the rest to botparse.
                else:
                    if (line[1] == 'PRIVMSG' or line[1] == 'NOTICE' or line[1] == 'KICK'):
                        Nick = Utils.getNick(line[0])
                        UHost = Utils.getHost(line[0])
                        Method = line[1]
                        Channel = line[2]
                        indices = 0, 1, 2
                        Victim = None
                        if Method == 'KICK':
                            Victim = line[3]
                            indices = 0, 1, 2, 3
                        e = list(string.join([i for j, i in enumerate(line) if j not in indices]))
                        e.pop(0)
                        Message = string.join(e, '')
                        MsgSplit = Message.split()
                        Parser.PCommandParser(Nick, UHost, Method, Victim, Channel, Message, MsgSplit)
                    else:
                        Parser.RawParse(line)
                        
    except KeyboardInterrupt:
        botCore.s.send("QUIT KeyboardInterrupt raised.\r\n")
        botCore.s.close()
        time.sleep(0.5)
        sys.exit('\n--- {0} KeyboardInterrupt'.format(config.tagC))
