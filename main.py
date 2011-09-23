#!/usr/bin/env python
# ^ been meaning to put that there for weeks now
import Core, Parser, Utils
import sys, time
import config

class __init__():
    readbuffer = ""
    Admin = Parser.Admin()
    bUtils = Utils.Utils()
    bParser = Parser.Parser()
    Core.connect()
    try:
        while True:
            readbuffer=readbuffer+Core.s.recv(1024)
            t = readbuffer.split("\r\n")
            readbuffer=t.pop()
            for line in t:
                line=line.split()
                bUtils.displayFormat(line)
                # these are more important, so use main to take care of them instead of botparse
                if(line[1]=="433"):
                    print '--- {0} Nick {1} is already taken!'.format(config.tagW, line[3])
                    Core.OurNick = config.AltNick
                    Core.register(config.AltNick)
                elif(line[1]=="001"):
                    print '--- {0} Successfully registered with IRCd.'.format(config.tagI)
                    Core.OurNick = config.Nick
                    Core.connectCmds()
                elif(line[0]=="PING"):
                    Core.s.send("PONG {0}\r\n".format(line[1]))
                    print '--- {0} PONGed server. ({1})'.format(config.tagI, line[1].strip(':'))
                elif(line[1] == "PRIVMSG" and bUtils.isChannel(line[2]) and line[3] == ":*rb"):
                    if Admin.Check(bUtils.getHost(line[0])):
                        print '--- {0} Reloading botparse.'.format(config.tagW)
                        Core.writeSock("PRIVMSG {0} :Okay, reloading parser and utils.\r\n".format(line[2]))
                        reload(Parser)
                        reload(Utils)
                        Admin = Parser.Admin()
                        bUtils = Utils.Utils()
                        bParser = Parser.Parser()
                    else:
                        Core.writeSock("PRIVMSG {0} :Permission denied.\r\n".format(line[2]))
                # pass the rest to botparse.
                else:
                    if (line[1] == 'PRIVMSG' or line[1] == 'NOTICE'):
                        try:
                            # format for parser.
                            Message = bUtils.getMessage(line, 0)
                            MsgSplit = Message.split()
                            bParser.CommandParser(bUtils.getNick(line[0]), bUtils.getHost(line[0]), line[1], line[2], Message, MsgSplit)
                        except IndexError:
                            # drop the message if it consists of only whitespace.
                            pass
                    elif line[1] == 'KICK':
                        Message = bUtils.getMessage(line, 1)
                        bParser.OnKick(bUtils.getNick(line[0]), bUtils.getHost(line[0]), line[2], line[3], Message)
                    else:
                        bParser.RawParse(line)
                        
    except KeyboardInterrupt:
        # remember to clear the queue before we abruptly quit
        Core.clearQueue()
        Core.s.send("QUIT KeyboardInterrupt raised.\r\n")
        Core.s.close()
        time.sleep(0.5)
        sys.exit('\n--- {0} KeyboardInterrupt'.format(config.tagC))
