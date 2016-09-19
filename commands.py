import random
import requests
import time
        
def greet(self):
    '''Greet'''
    self.irc.send('PRIVMSG ' + self.channel + ' :Hello there. \n')

def backlog(self):
    '''Backlog grabber'''
    self.update_logs()
    logfile = open('rawlogs.log', 'rb')
    linesback = 0
    pointer = 0
    backlog = open('backlog.log', 'w+')
    while linesback < 200:
        logfile.seek(-pointer,2)
        newlinecheck = logfile.read(1)
        if(newlinecheck == '\n'):
            linesback += 1
        pointer += 1
    for line in logfile.readlines():
        if line.find('PRIVMSG ' + self.channel) != -1:
            backlog.write('<' + line[line.find(':')+1:line.find('!')] + '> ')
            backlog.write(line[line.find(self.channel + ' :') + len(self.channel + ' :'):])
        if line.find('PART ' + self.channel + ' :') != -1: 
            backlog.write(line[line.find(':')+1:line.find('!')] + ' has parted ' + self.channel + '. Quit message: ' + line[line.find(self.channel + ' :') + len(self.channel + ' :\n') - 1:])
        if line.find('JOIN :' + self.channel) != -1: 
            backlog.write(line[line.find(':')+1:line.find('!')] + ' has joined ' + self.channel + '.\n')
    backlog.seek(0)
    pastedata = {'api_dev_key': '57118c0169e20c0f77a629cb1e3455da', 'api_option': 'paste', 'api_paste_code': backlog.read(), 'api_paste_expire_date': '1H', 'api_paste_private': '1'}
    pastebin = requests.post('http://pastebin.com/api/api_post.php', pastedata)
    self.irc.send('PRIVMSG ' + self.channel + ' :' + pastebin.text + '\n')
    logfile.close()

def exalteddice(self, read):
    '''Dice bot'''
    roller = read[read.find(':')+1:read.find('!')]
    successes = 0 
    crits = 0
    rollcount = 0
    rolls = int(read[read.find('!ex ') + 4:read.find('!ex ')+6])
    self.irc.send('PRIVMSG ' + self.channel + ' :<' + str(roller) + '> has rolled ' + str(rolls) + ' dice. [')
    while rolls >= rollcount: 
        rollcount += 1
        result = random.randint(1, 10)
        if result >= 7: 
            self.irc.send('\x02')
            successes += 1
        if result == 10:
            crits += 1
        if rollcount != rolls:
            self.irc.send(str(result) + ', ')
        if result >= 7: 
            self.irc.send('\x02')
        if rollcount == rolls:
            self.irc.send(str(result) + '] \x02' + str(successes + crits) + ' hits.\x02 Damage roll: ' + str(successes) + '\n')
            break

def markov(self):
    '''Markov speech'''
    logfile = open('rawlogs.log', 'r')
    markovlist = {}
    lastword = ''
    wordchain = []
    chainedword = ''
    wisdom = ''
    wisdomlength = random.randint(10,25)
    wisdomcount = 0
    for line in logfile.readlines():
        if line.find('PRIVMSG ' + self.channel + ' :') != -1:
            for word in line[line.find('PRIVMSG ' + self.channel + ' :') + len('PRIVMSG ' + self.channel + ' :'):].split():
                if lastword not in markovlist:
                    markovlist[lastword] = [word]
                    if len(wordchain) > 1: 
                        markovlist[' '.join(wordchain)] = [word]
                else:
                    markovlist[lastword] += [word]
                wordchain += [word]
                if len(wordchain) <= random.randint(3,10):
                    if chainedword not in markovlist:
                        markovlist[chainedword] = [' '.join(wordchain)]
                    else:
                        markovlist[chainedword] += [' '.join(wordchain)]
                else:
                    chainedword = word
                    wordchain = []
                lastword = word
    lastword = random.choice(markovlist.keys())
    wisdom += lastword + ' '
    while wisdomcount <= wisdomlength:
        if lastword in markovlist:
            lastword = markovlist[lastword][random.randint(0, len(markovlist[lastword]) - 1)]
        else:
            lastword = random.choice(markovlist.keys())
        wisdom += str(lastword) + ' '
        wisdomcount += 1
    self.irc.send('PRIVMSG ' + self.channel + ' :' + wisdom + '\n')
    logfile.close()