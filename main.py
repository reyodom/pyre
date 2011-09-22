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
                Utils.displayFormat(line)
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
                # pass the rest to botparse.
                else:
                    if (line[1] == 'PRIVMSG' or line[1] == 'NOTICE'):
                        try:
                            # format for parser.
                            Message = Utils.getMessage(line, 0)
                            MsgSplit = Message.split()
                            Parser.CommandParser(Utils.getNick(line[0]), Utils.getHost(line[0]), line[1], line[2], Message, MsgSplit)
                        except IndexError:
                            # drop the message if it consists of only whitespace.
                            pass
                    elif line[1] == 'KICK':
                        Message = Utils.getMessage(line, 1)
                        Parser.OnKick(Utils.getNick(line[0]), Utils.getHost(line[0]), line[2], line[3], Message)
                    else:
                        Parser.RawParse(line)
                        
    except KeyboardInterrupt:
        # remember to clear the queue before we abruptly quit
        botCore.clearQueue()
        botCore.s.send("QUIT KeyboardInterrupt raised.\r\n")
        botCore.s.close()
        time.sleep(0.5)
        sys.exit('\n--- {0} KeyboardInterrupt'.format(config.tagC))
