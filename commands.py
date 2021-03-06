import random
import requests
import time

def identify(self, read):
    if read.find('PRIVMSG #'):
        channel = read[read.find('PRIVMSG') + 8:read.find(' :')]
        if read.find('Hi Bubble') != -1:
            greet(self, channel)
        if read.find('ey bubble') + read.find('ey Bubble') != -2: 
            markov(self, channel)
        if read.find('!context') != -1:
            backlog(self, channel)
        if read.find('!ex') != -1: 
            exalteddice(self, channel, read)
        
def greet(self, channel):
    '''Greet'''
    self.send_message('Hello there.', channel)

def backlog(self, channel):
    '''Backlog grabber'''
    self.update_logs()
    logfile = open('rawlogs.log', 'rb')
    linesback = 0
    pointer = 0
    backlog = open('backlog.log', 'w+')
    while linesback < 250:
        try:
            logfile.seek(-pointer,2)
            newlinecheck = logfile.read(1)
            if(newlinecheck == '\n'):
                linesback += 1
            pointer += 1
        except IOError:
            break
    for line in self.logify_text(channel, logfile.readlines()):
        backlog.write(line)
    backlog.seek(0)
    pastedata = {'api_dev_key': '57118c0169e20c0f77a629cb1e3455da', 'api_option': 'paste', 'api_paste_code': backlog.read(), 'api_paste_expire_date': '1H', 'api_paste_private': '1'}
    pastebin = requests.post('http://pastebin.com/api/api_post.php', pastedata)
    self.send_message(pastebin.text, channel)
    logfile.close()

def exalteddice(self, channel, read):
    '''Dice bot'''
    roller = read[read.find(':')+1:read.find('!')]
    successes = 0 
    crits = 0
    rollcount = 0
    rolls = int(read[read.find('!ex ') + 4:read.find('!ex ')+6])
    response = '<' + str(roller) + '> has rolled ' + str(rolls) + ' dice. ['
    while rolls >= rollcount: 
        rollcount += 1
        result = random.randint(1, 10)
        if result >= 7: 
            response += '\x02'
            successes += 1
        if result == 10:
            crits += 1
        response += str(result)
        if rollcount != rolls:
            response += ', '
        if result >= 7: 
            response += '\x02'
        if rollcount == rolls:
            response += '] \x02' + str(successes + crits) + ' hits.\x02 Damage roll: ' + str(successes)
            self.send_message(response, channel)
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
    self.send_message(wisdom, channel)
    logfile.close()