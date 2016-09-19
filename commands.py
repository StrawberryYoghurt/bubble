import random
import requests
import time
        
def greet(self, channel):
    '''Greet'''
    self.irc.send('PRIVMSG ' + channel + ' :Hello there. \n')

def backlog(self, channel):
    '''Backlog grabber'''
    self.update_logs()
    logfile = open('rawlogs.log', 'rb')
    linesback = 0
    pointer = 0
    backlog = open('backlog.log', 'w+')
    while linesback < 200:
        try:
            logfile.seek(-pointer,2)
            newlinecheck = logfile.read(1)
            if(newlinecheck == '\n'):
                linesback += 1
            pointer += 1
        except:
            pass
    for line in logfile.readlines():
        if line.find('PRIVMSG ' + channel) != -1:
            backlog.write('<' + line[line.find(':')+1:line.find('!')] + '> ')
            backlog.write(line[line.find(channel + ' :') + len(channel + ' :'):])
        if line.find('PART ' + channel + ' :') != -1: 
            backlog.write(line[line.find(':')+1:line.find('!')] + ' has parted ' + channel + '. Quit message: ' + line[line.find(channel + ' :') + len(channel + ' :\n') - 1:])
        if line.find('JOIN :' + channel) != -1: 
            backlog.write(line[line.find(':')+1:line.find('!')] + ' has joined ' + channel + '.\n')
    backlog.seek(0)
    pastedata = {'api_dev_key': '57118c0169e20c0f77a629cb1e3455da', 'api_option': 'paste', 'api_paste_code': backlog.read(), 'api_paste_expire_date': '1H', 'api_paste_private': '1'}
    pastebin = requests.post('http://pastebin.com/api/api_post.php', pastedata)
    self.irc.send('PRIVMSG ' + channel + ' :' + pastebin.text + '\n')
    logfile.close()

def exalteddice(self, channel, read):
    '''Dice bot'''
    roller = read[read.find(':')+1:read.find('!')]
    successes = 0 
    crits = 0
    rollcount = 0
    rolls = int(read[read.find('!ex ') + 4:read.find('!ex ')+6])
    self.irc.send('PRIVMSG ' + channel + ' :<' + str(roller) + '> has rolled ' + str(rolls) + ' dice. [')
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

def markov(self, channel):
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
        if line.find('PRIVMSG ' + channel + ' :') != -1:
            for word in line[line.find('PRIVMSG ' + channel + ' :') + len('PRIVMSG ' + channel + ' :'):].split():
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
    self.irc.send('PRIVMSG ' + channel + ' :' + wisdom + '\n')
    logfile.close()