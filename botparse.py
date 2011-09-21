import string, re, time, sys, socket
from datetime import datetime

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
    
    def colour(self, input, colour, style=0):
        if colour == 'black':
            return '\033[{2};{0}m{1}\033[0m'.format('30', input, style)
        if colour == 'red':
            return '\033[{2};{0}m{1}\033[0m'.format('31', input, style)
        if colour == 'green':
            return '\033[{2};{0}m{1}\033[0m'.format('32', input, style)
        if colour == 'yellow':
            return '\033[{2};{0}m{1}\033[0m'.format('33', input, style)
        if colour == 'blue':
            return '\033[{2};{0}m{1}\033[0m'.format('34', input, style)
        if colour == 'pink':
            return '\033[{2};{0}m{1}\033[0m'.format('35', input, style)
        if colour == 'cyan':
            return '\033[{2};{0}m{1}\033[0m'.format('36', input, style)
        if colour == 'white':
            return '\033[{2};{0}m{1}\033[0m'.format('37', input, style)
            
    def getMessage(self, line, type=0, dnp=0):
        '''
        This does something, I'm just not sure what it is...'
        '''
        if type == 1:
            indices = 0, 1, 2, 3
        elif type == 2:
            indices = 0, 1
        elif type == 3:
            indices = 0, 1, 2, 3, 4
        else:
            indices = 0, 1, 2
        try:
            e = list(string.join([i for j, i in enumerate(line) if j not in indices]))
            if (dnp == 0):
                e.pop(0)
            Message = string.join(e, '')
            return Message
        except IndexError:
            return ''
    
    def displayFormat(self, line):
        if line[0] == 'PING' \
        or '00' in line[1] \
        or '25' in line[1] \
        or '26' in line[1] \
        or '37' in line[1] \
        or '433' in line[1] \
        or '366' in line[1]:
            pass
        elif line[1] == 'NOTICE' and line[2] == 'AUTH':
            pass
        elif line[1] == 'KICK':
            print '* {0}!{1} kicked {2} out of {3} ({4}).'.format(self.colour(self.getNick(line[0]), 'green', 1),
            self.colour(self.getHost(line[0]), 'green'),
            self.colour(line[3], 'green'),
            self.colour(line[2], 'cyan'),
            self.getMessage(line, 1))
        elif line[1] == 'PART':
            if (self.getNick(line[0]) == botCore.OurNick):
                print '* I left {0}. ({1})'.format(self.colour(line[2], 'cyan'),
                self.getMessage(line, 0))
            else:
                print '* {0}!{1} left {2} ({3}).'.format(self.colour(self.getNick(line[0]), 'green', 1),
                self.colour(self.getHost(line[0]), 'green'),
                self.colour(line[2], 'cyan'),
                self.getMessage(line, 0))
        elif line[1] == 'QUIT':
            print '* {0}!{1} left IRC. ({2})'.format(self.colour(self.getNick(line[0]), 'green', 1),
            self.colour(self.getHost(line[0]), 'green'),
            self.getMessage(line, 2))
        elif line[1] == 'NICK':
            if (self.getNick(line[0]) == botCore.OurNick):
                print '* My nick was changed to {0}.'.format(self.colour(self.getMessage(line, 2), 'green', 1))
                botCore.OurNick = self.getMessage(line, 2)
            else:
                print '* {0}!{1} changed nick to {2}.'.format(self.colour(self.getNick(line[0]), 'green', 1),
                self.colour(self.getHost(line[0]), 'green'),
                self.colour(self.getMessage(line, 2), 'green', 1))
        elif line[1] == 'JOIN':
            if (self.getNick(line[0]) == botCore.OurNick):
                print '* I joined {0}.'.format(self.colour(line[2].lstrip(':'), 'cyan'))
                print '-----'
            else:
                print '* {0}!{1} joined {2}.'.format(self.colour(self.getNick(line[0]), 'green', 1),
                self.colour(self.getHost(line[0]), 'green'),
                self.colour(line[2].lstrip(':'), 'cyan'))
        elif line[1] == 'NOTICE':
            print '[NOTICE] {0} -> {1}: {2}'.format(self.colour(self.getNick(line[0]), 'green', 1),
            self.colour(line[2].strip(':'), 'cyan'),
            self.getMessage(line, 0))
        elif line[1] == 'PRIVMSG':
            print '{1}: <{0}> {2}'.format(self.colour(self.getNick(line[0]), 'green'),
            self.colour(line[2], 'cyan'),
            self.getMessage(line, 0))
        elif line[1] == '332':
            print '* \033[1mTopic for\033[0m {0}: {1}'.format(self.colour(line[3], 'cyan', 0), self.getMessage(line, 1))
        elif line[1] == '333':
            print(datetime.fromtimestamp(int(line[5])).strftime('* Set by {0} on \033[1m%d %B %Y\033[0m at \033[1m%I:%M:%S %p\033[0m')).format(self.colour(line[4], 'green'))
        elif line[1] == '353':
            print '* Users on {0}: {1}'.format(line[4], self.getMessage(line, 3))
            print '-----'
        elif line[1] == 'MODE':
            print '* {0}!{1} sets mode on {2}: {3}'.format(self.colour(self.getNick(line[0]), 'green', 1),
            self.colour(self.getHost(line[0]), 'green'),
            self.colour(line[2], 'cyan'),
            self.getMessage(line, 0, 1))
        else:
            print self.colour(string.join(line), 'black')

class Parser():
    def CommandParser(self, Nick, UHost, Method, Channel, Message, MsgSplit):
        if(Nick in config.Ignores):
            return None
        elif Method == "PRIVMSG" and Utils().isChannel(Channel):
            if Message == "dicks":
                botCore.writeSock("PRIVMSG {0} :dildos\r\n".format(Channel))
                return None 
            elif Message == "dildos":
                botCore.writeSock("PRIVMSG {0} :dicks\r\n".format(Channel))
                return None 
            elif Message == "h":
                botCore.writeSock("PRIVMSG {0} :h\r\n".format(Channel))
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
            elif Message == "*stitime":
                botCore.writeSock("PRIVMSG {0} :{1}\r\n".format(Channel, stitime.stiTime()))
                return None
            elif MsgSplit[0] == "*lookup":
                try:
                    dnslookup.detect(Nick, Channel, MsgSplit[1])
                    return None
                except IndexError:
                    botCore.writeSock("PRIVMSG {0} :Not enough arguments.\r\n".format(Channel))
            elif MsgSplit[0] == "*cc":
                try:
                    test=MsgSplit[3]
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
                        if (MsgSplit[1] not in botCore.JoinedChannels):
                            botCore.writeSock("JOIN {0}\r\n".format(MsgSplit[1]))
                        else:
                            botCore.writeSock("PRIVMSG {0} :I'm already on {1}, you derp.\r\n".format(Channel, MsgSplit[1]))
                        return None
                    except IndexError:
                        botCore.writeSock("PRIVMSG {0} :No channel specified.\r\n".format(Channel))
                        return None 
                else:
                    botCore.writeSock("PRIVMSG {0} :You don't have permission to do that.\r\n".format(Channel))
                    return None 
            elif MsgSplit[0] == "*leave":
                if Admin().Check(UHost):
                    try:
                        test=MsgSplit[1]
                        if (MsgSplit[1] in botCore.JoinedChannels):
                            botCore.writeSock("PART {0} :wherp\r\n".format(MsgSplit[1]))
                        else:
                            botCore.writeSock("PRIVMSG {0} :I'm not on {1}, you derp.\r\n".format(Channel, MsgSplit[1]))
                        return None
                    except IndexError:
                        botCore.writeSock("PRIVMSG {0} :No channel specified.\r\n".format(Channel))
                        return None 
                else:
                    botCore.writeSock("PRIVMSG {0} :You don't have permission to do that.\r\n".format(Channel))
                    return None
            elif MsgSplit[0] == "*nick":
                if Admin().Check(UHost):
                    try:
                        test=MsgSplit[1]
                        botCore.writeSock("NICK :{0}\r\n".format(MsgSplit[1]))
                        return None
                    except IndexError:
                        botCore.writeSock("PRIVMSG {0} :Specify a nick.\r\n".format(Channel))
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
        elif (line[1] == 'JOIN' and Utils().getNick(line[0]) == botCore.OurNick):
            botCore.JoinedChannels.append(line[2].lstrip(':'))
        elif (line[1] == 'PART' and Utils().getNick(line[0]) == botCore.OurNick):
            try: 
                botCore.JoinedChannels.remove(line[2])
            except:
                print '???'
        else:
            return None
    
    def OnKick(self, Kicker, KHost, Channel, Victim, Reason):
        if(Victim == botCore.OurNick):
            print '--- {0} I was kicked from {1} by {2}.'.format(config.tagW, Channel, Kicker)
            if config.kickRejoin == True:
                time.sleep(2)
                botCore.writeSock("JOIN {0}\r\n".format(Channel))
                return None
            else:
                return None

import botCore
import kawaii
import Currency
import tripcode
import config      
# import floodController
import stitime
import dnslookup