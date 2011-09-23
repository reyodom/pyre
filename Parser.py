import string, re, time, sys, socket
from datetime import datetime
from Utils import Utils

Utils = Utils()

class Admin():
    def __init__(self):
        adminfile = open('admins')
        self.admins = adminfile.readlines()
        adminfile.close()
        for i, admin in enumerate(self.admins):
            self.admins[i]=admin.rstrip("\n")
    
    def Check(self, input):
        '''see if input is in the admin list, input being a uhost'''
        if input in self.admins:
            return True
        else:
            return False
            
    def Add(self, adder, channel, host):
        '''Adds an admin, where adder is the nick of the issuer and host is the uhost of the new admin.'''
        if ('@' not in host) or (host.count('@') > 1):
            Core.writeSock("PRIVMSG {0} :'{1}' is not a valid user@host.\r\n".format(channel, host))
            print '--- {0} {1} tried to add \'{2}\' to the admin list.'.format(config.tagW, adder, host)
            return None
        adminfile = open('admins', 'r')
        admins = adminfile.readlines()
        if (host in admins) or ('{0}\n'.format(host) in admins):
            Core.writeSock("PRIVMSG {0} :'{1}' is already in the admin list!\r\n".format(channel, host))
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
        self.admins.append(host)
        Core.writeSock("PRIVMSG {0} :'{1}' was added to the admin list.\r\n".format(channel, host))

class Parser():
    def CommandParser(self, Nick, UHost, Method, Channel, Message, MsgSplit):
        if (Nick in config.Ignores):
            return None
        elif Method == "PRIVMSG" and Utils.isChannel(Channel):
            if Message == "dicks":
                Core.writeSock("PRIVMSG {0} :dildos\r\n".format(Channel))
                return True
            elif Message == "dildos":
                Core.writeSock("PRIVMSG {0} :dicks\r\n".format(Channel))
                return True
            elif Message == "h":
                Core.writeSock("PRIVMSG {0} :h\r\n".format(Channel))
                return True
            elif MsgSplit[0] == "*trip":
                #try:
                password = MsgSplit
                password.pop(0)
                tripcode.Make(Core.writeSock, Channel, string.lstrip(string.join(password), '#'))
                return True
                #except:
                #    Core.writeSock("PRIVMSG {0} :An error occurred.\r\n".format(Channel))
                #    return False 
            elif Message == "*version":
                Core.writeSock("PRIVMSG {0} :.-.\r\n".format(Channel))
                return True 
            elif Message == "brb":
                Core.writeSock("PRIVMSG {0} :See you later, {1}-kun.\r\n".format(Channel, Nick))
                return True
            elif Message == "*stitime":
                stitime.stiTime(Core.writeSock, Channel)
                return True
            elif MsgSplit[0] == "*lookup":
                try:
                    dnslookup.detect(Core.writeSock, Nick, Channel, MsgSplit[1])
                    return True
                except IndexError:
                    Core.writeSock("PRIVMSG {0} :Not enough arguments.\r\n".format(Channel))
                    return False
            elif MsgSplit[0] == "*cc":
                try:
                    test=MsgSplit[3]
                    Currency.currencyConvert(Core.writeSock, Nick, Channel, MsgSplit[1], MsgSplit[2], MsgSplit[3])
                    return True 
                except IndexError:
                    Core.writeSock('PRIVMSG {0} :That\'s not correct syntax.\r\n'.format(Channel))
                    return False
            elif 'weeaboo' in Message or 'kawaii' in Message:
                kawaii.sendFace(Channel, Core.writeSock)
                return True 
            elif re.search(".*\\ when\\ was\\ .*lobby\\ .*\\ good.*\\Z(?ms)", Message) or re.search(".*\\ when\\ .*lobby\\ was\\ good.*\\Z(?ms)", Message) or re.search('was\\ .*lobby\\ .*\\ good.*\\Z(?ms)', Message):
                Core.writeSock("PRIVMSG {0} :#lobby was never good.\r\n".format(Channel))
                return True
            elif MsgSplit[0] == "*join":
                if Admin().Check(UHost):
                    try:
                        test=MsgSplit[1]
                        if (MsgSplit[1] not in Core.JoinedChannels):
                            Core.writeSock("JOIN {0}\r\n".format(MsgSplit[1]))
                            return True
                        else:
                            Core.writeSock("PRIVMSG {0} :I'm already on {1}, you derp.\r\n".format(Channel, MsgSplit[1]))
                        return False
                    except IndexError:
                        Core.writeSock("PRIVMSG {0} :No channel specified.\r\n".format(Channel))
                        return False
                else:
                    Core.writeSock("PRIVMSG {0} :You don't have permission to do that.\r\n".format(Channel))
                    return False
            elif MsgSplit[0] == "*leave":
                if Admin().Check(UHost):
                    try:
                        test=MsgSplit[1]
                        if (MsgSplit[1] in Core.JoinedChannels):
                            Core.writeSock("PART {0} :wherp\r\n".format(MsgSplit[1]))
                            return True
                        else:
                            Core.writeSock("PRIVMSG {0} :I'm not on {1}, you derp.\r\n".format(Channel, MsgSplit[1]))
                        return False
                    except IndexError:
                        Core.writeSock("PRIVMSG {0} :No channel specified.\r\n".format(Channel))
                        return False
                else:
                    Core.writeSock("PRIVMSG {0} :You don't have permission to do that.\r\n".format(Channel))
                    return None
            elif MsgSplit[0] == "*nick":
                if Admin().Check(UHost):
                    try:
                        test=MsgSplit[1]
                        Core.writeSock("NICK :{0}\r\n".format(MsgSplit[1]))
                        return True
                    except IndexError:
                        Core.writeSock("PRIVMSG {0} :Specify a nick.\r\n".format(Channel))
                        return False 
                else:
                    Core.writeSock("PRIVMSG {0} :You don't have permission to do that.\r\n".format(Channel))
                    return False
            elif Message == "*ra":
                if Admin().Check(UHost):
                    Admin().__init__()
                    print '--- {0} Reloading access list.'.format(config.tagW)
                    Core.writeSock("PRIVMSG {0} :Reloaded access list.\r\n".format(Channel))
                    return True 
                else:
                    Core.writeSock("PRIVMSG {0} :You don't have permission to do that.\r\n".format(Channel))
                    return False
            elif MsgSplit[0] == "*aa":
                if Admin().Check(UHost):
                    Admin().Add(Nick, Channel, MsgSplit[1])
                    return True
                else:
                    Core.writeSock("PRIVMSG {0} :You don't have permission to do that.\r\n".format(Channel))
                    return False
            elif(Message == "*quit"):
                if Admin().Check(UHost.strip()):
                    # remember to clear the queue before we abruptly quit
                    Core.clearQueue()
                    Core.s.send("PRIVMSG {0} :Quitting now...\r\n".format(Channel))
                    Core.s.send("QUIT Bye!\r\n")
                    time.sleep(1)
                    Core.s.close()
                    sys.exit('--- {0} *quit command issued.'.format(config.tagC))
                else:
                     Core.writeSock("PRIVMSG {0} :You don't have permission to do that.\r\n".format(Channel))
                     return False 
            else:
                return None      
        else:
            return None
            
    def RawParse(self, line):
        if (line[0] == 'ERROR'):
            print '--- {0} Disconnected from IRC. Attempting reconnect in 5 seconds...'.format(config.tagC)
            time.sleep(5)
            Core.s.close()
            Core.s = socket.socket( )
            Core.connect()
        elif (line[1] == 'JOIN' and Utils.getNick(line[0]) == Core.OurNick):
            Core.JoinedChannels.append(line[2].lstrip(':'))
        elif (line[1] == 'PART' and Utils.getNick(line[0]) == Core.OurNick):
            try: 
                Core.JoinedChannels.remove(line[2])
            except:
                print '???' 
        elif line[1] == 'NICK':
            if (Utils.getNick(line[0]) == Core.OurNick):
                Core.OurNick = Utils.getMessage(line, 2)
            else:
                pass
        else:
            return None
    
    def OnKick(self, Kicker, KHost, Channel, Victim, Reason):
        if(Victim == Core.OurNick):
            print '--- {0} I was kicked from {1} by {2}.'.format(config.tagW, Channel, Kicker)
            if config.kickRejoin == True:
                Core.writeSock("JOIN :{0}\r\n".format(Channel))
                return True
            else:
                return None

import Core
from modules import kawaii, Currency, tripcode, stitime, dnslookup
kawaii = kawaii.Weeaboo()
import config      
