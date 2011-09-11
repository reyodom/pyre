import string
import re
import time
import sys
import socket

class Admin():
    def Load(self):
        global admins
        adminfile = open('admins')
        admins = adminfile.readlines()
        adminfile.close()
        for i, admin in enumerate(admins):
            admins[i]=admin.rstrip("\n")
    
    def Check(self, input):
        global admins
        if input in admins:
            return True
        else:
            return False
            
    def Add(self, adder, channel, host):
        if ('@' not in host) or (host.count('@') > 1):
            botCore.writeSock("PRIVMSG {0} :'{1}' is not a valid user@host.\r\n".format(channel, host))
            print '--- {0} {1} tried to add \'{2}\' to the admin list.'.format(config.tagW, adder, host)
            return None
        adminfile = open('admins', 'r')
        admins = adminfile.readlines()
        if (host in admins) or ('{0}\n'.format(host) in admins):
            botCore.writeSock("PRIVMSG {0} :'{1}' is already in the admin list!\r\n".format(channel, host))
            print '--- {0} {1} tried to add \'{2}\' to the admin list.'.format(config.tagW, adder, host)
            return None
        adminfile.close()
        adminfile = open('admins', 'a')
        size = len(admins)-1
        if '\n' in admins[size]:
            pass
        else:
            adminfile.write('\n')
        adminfile.write('{0}\n'.format(host))
        adminfile.close()
        print '--- {0} {1} added \'{2}\' to the admin list.'.format(config.tagW, adder, host)
        Admin().Load()
        botCore.writeSock("PRIVMSG {0} :'{1}' was added to the admin list.\r\n".format(channel, host))

class Utils():
    floodC = 0
    
    def resetFloodCount(self):
        if (Utils().floodC > 0):
            Utils().floodC = 0
            return True
        else:
            return False

    def getNick(self, input):
        n=input.partition('!')
        return n[0].strip(':')
        
    def isChannel(self, input):
        if '#' in input:
            return True
        else:
            return False
        
    def getHost(self, input):
        h=input.partition('!')
        return h[2]
                
    def getIdent(self, input):
        j=string.split(input, "@")
        j=string.split(j[0], "!")
        return j[1]

class Parser():
    def PCommandParser(self, Nick, UHost, Method, Victim, Channel, Message, MsgSplit):
        if(Nick in config.Ignores):
            return None
        if(Method == "KICK" and Victim == "Lyra"):
            print '--- {0} I was kicked from {1} by {2}.'.format(config.tagW, Channel, Nick)
            time.sleep(2)
            botCore.writeSock("JOIN {0}\r\n".format(Channel))
            return None 
        elif Method == "PRIVMSG" and Utils().isChannel(Channel):
            if Message == "dicks":
                botCore.writeSock("PRIVMSG {0} :dildos\r\n".format(Channel))
                return None 
            elif Message == "dildos":
                botCore.writeSock("PRIVMSG {0} :dicks\r\n".format(Channel))
                return None 
            elif MsgSplit[0] == "*trip":
                try:
                    password = MsgSplit
                    password.pop(0)
                    output = tripcode.Make(string.lstrip(string.join(password), '#'))
                    botCore.writeSock("PRIVMSG {0} :\x02Tripcode: !\x02{1}\r\n".format(Channel, output))
                    return None 
                except:
                    botCore.writeSock("PRIVMSG {0} :An error occurred.\r\n".format(Channel))
                    return None 
            elif Message == "*version":
                botCore.writeSock("PRIVMSG {0} :stal's pybot, version 5.2 \"Palladium\"\r\n".format(Channel))
                return None 
            elif Message == "brb":
                botCore.writeSock("PRIVMSG {0} :See you later, {1}-kun.\r\n".format(Channel, Nick))
                return None 
            elif MsgSplit[0] == "*cc":
                try:
                    test=MsgSplit[4]
                    Currency.currencyConvert(Nick, Channel, MsgSplit[1], MsgSplit[2], MsgSplit[3])
                    return None 
                except IndexError:
                    botCore.writeSock('PRIVMSG {0} :That\'s not correct syntax.\r\n'.format(Channel))
                    return None 
            elif 'weeaboo' in Message or 'kawaii' in Message:
                if kawaii.facesAreLoaded == 'no':
                    kawaii.loadfaces()
                botCore.writeSock("PRIVMSG {0} :{1}\r\n".format(Channel, kawaii.getface())) 
                return None 
            elif re.search(".*\\ when\\ was\\ .*lobby\\ .*\\ good.*\\Z(?ms)", Message) or re.search(".*\\ when\\ .*lobby\\ was\\ good.*\\Z(?ms)", Message) or re.search('was\\ .*lobby\\ .*\\ good.*\\Z(?ms)', Message):
                botCore.writeSock("PRIVMSG {0} :#lobby was never good.\r\n".format(Channel))
                return None 
            elif MsgSplit[0] == "*join":
                if Admin().Check(UHost):
                    try:
                        test=MsgSplit[1]
                        botCore.writeSock("JOIN {0}\r\n".format(MsgSplit[1]))
                        return None
                    except IndexError:
                        botCore.writeSock("PRIVMSG {0} :No channel specified.\r\n".format(Channel))
                        return None 
                else:
                    botCore.writeSock("PRIVMSG {0} :You don't have permission to do that.\r\n".format(Channel))
                    return None 
            elif Message == "*ra":
                if Admin().Check(UHost):
                    Admin().Load()
                    print '--- {0} Reloading access list.'.format(config.tagW)
                    botCore.writeSock("PRIVMSG {0} :Reloaded access list.\r\n".format(Channel))
                    return None 
                else:
                    botCore.writeSock("PRIVMSG {0} :You don't have permission to do that.\r\n".format(Channel))
                    return None 
            elif MsgSplit[0] == "*aa":
                if Admin().Check(UHost):
                    Admin().Add(Nick, Channel, MsgSplit[1])
                else:
                    botCore.writeSock("PRIVMSG {0} :You don't have permission to do that.\r\n".format(Channel))
            elif(Message == "*quit"):
                if Admin().Check(UHost.strip()):
                    botCore.writeSock("PRIVMSG {0} :Bye!\r\n".format(Channel))
                    botCore.writeSock("QUIT Bye!\r\n")
                    botCore.s.close()
                    sys.exit('--- {0} *quit command issued.'.format(config.tagC))
                else:
                     botCore.writeSock("PRIVMSG {0} :You don't have permission to do that.\r\n".format(Channel))
                     return None   
            else:
                return None      
        else:
            return None
            
    def RawParse(self, line):
        if (line[0] == 'ERROR'):
            print '--- {0} Disconnected from IRC. Attempting reconnect in 5 seconds...'.format(config.tagC)
            time.sleep(5)
            botCore.s.close()
            botCore.s = socket.socket( )
            botCore.connect()
        else:
            return None

import botCore
import kawaii
import Currency
import tripcode
import config      
import floodController