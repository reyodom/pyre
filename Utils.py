import Core
from datetime import datetime

class Utils():
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
        '''
        ANSI-style colouring.
        '''
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
            import string
            e = list(string.join([i for j, i in enumerate(line) if j not in indices]))
            if (dnp == 0):
                e.pop(0)
            Message = string.join(e, '')
            return Message
        except IndexError:
            return ''
    
    def displayFormat(self, line):
        '''
        Format lines for terminal output.
        '''
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
            if (self.getNick(line[0]) == Core.OurNick):
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
            if (self.getNick(line[0]) == Core.OurNick):
                print '* My nick was changed to {0}.'.format(self.colour(self.getMessage(line, 2), 'green', 1))
                Core.OurNick = self.getMessage(line, 2)
            else:
                print '* {0}!{1} changed nick to {2}.'.format(self.colour(self.getNick(line[0]), 'green', 1),
                self.colour(self.getHost(line[0]), 'green'),
                self.colour(self.getMessage(line, 2), 'green', 1))
        elif line[1] == 'JOIN':
            if (self.getNick(line[0]) == Core.OurNick):
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
