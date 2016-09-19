import socket
import ssl
import time
import os.path
import threading
from commands import *

class Connection:
    def __init__(self, server, port, nick, ident, realname, password):
        self.nick = nick
        self.nick = nick
        self.ident = ident
        self.realname = realname
        self.password = password
        self.host = (server, port)
        self.ircbase = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc = ssl.wrap_socket(self.ircbase)
        self.connectedto = []
        self.backlog = ['###Starting new log session###']
        self.logswitch = False
        self.read = []

    def connect_server(self):
        self.check_logfile()
        self.irc.connect(self.host)
        self.send('NICK ' + self.nick + '\n')
        self.send('USER ' + self.ident + ' ' + str(self.host) + ' ' + self.realname + '\n')
        if self.password != False:
            self.send('PRIVMSG nickserv :identify ' + self.password + '\n')
        self.to_terminal("Connected.")
        time.sleep(10)

    def join_channel(self, channel):
        self.check_logfile(channel + '.log')
        self.send('JOIN ' + channel + '\n')
        self.to_terminal('Joining channel ' + channel)
        if channel not in self.connectedto:
            self.connectedto += [channel]
        print 'Joined ' + channel

    def start(self):
        self.irc.settimeout(260)
        try:
            while True:
                self.read = self.irc.recv(500)
                self.to_terminal(self.read)
                identify(self, self.read)
                if self.read.find('PING') != -1:
                    self.send('PONG ' + self.read.split() [1] + '\n')
                if self.logswitch == False and self.read.find('PING :') == -1:
                    logger = threading.Timer(10, self.update_logs)
                    logger.start()
                    self.logswitch = True
        except KeyboardInterrupt: 
            self.send(raw_input('Enter your input: '))
            self.start()

    def update_logs(self):
        for channel in self.connectedto:
            logs = open(channel + '.log', 'ab')
            for line in self.backlog:
                if line.find('###Starting new log session###') != -1:
                    logs.write('\n###Starting new log session ### ' + self.get_timestamp() + '###\n\n')
                elif line.find('PRIVMSG ' + channel) != -1:
                    logs.write(self.get_timestamp() + '<' + line[line.find(':')+1:line.find('!')] + '> ')
                    logs.write(line[line.find(channel + ' :') + len(channel + ' :'):])
                elif line.find('PART ' + channel + ' :') != -1: 
                    logs.write(self.get_timestamp() + line[line.find(':')+1:line.find('!')] + ' has parted ' + channel + '. Quit message: ' + line[line.find(channel + ' :') + len(channel + ' :\n') - 1:])
                elif line.find('JOIN :' + channel + ' :') != -1: 
                    logs.write(self.get_timestamp() + line[line.find(':')+1:line.find('!')] + ' has joined ' + channel + '.\n')
            logs.close()
        logs = open('rawlogs.log', 'ab')
        for line in self.backlog:
            logs.write(line)
        logs.close()
        self.backlog = []
        print 'Logs updated.'
        self.logswitch = False

    def to_terminal(self, content):
        if content.find('\n') != -1:
            print self.get_timestamp() + content[:content.find('\n')]
        else:
            print self.get_timestamp() + content
        self.backlog += [content]

    def send_message(self, content, target):
        self.irc.send('PRIVMSG ' + target + ' :' + content + '\n')
        self.to_terminal('Sent to ' + target + ': ' + content)

    def send(self, content):
        self.irc.send(content + '\n')
        self.to_terminal('Sent: ' + content)

    def get_timestamp(self):
        return time.asctime(time.gmtime(time.time())) + ' * '

    def check_logfile(self, filename = "rawlogs.log"):
        if not os.path.isfile(filename):
            newlogs = open(filename, 'w')
            newlogs.write("Generating a new log file. \n\n\n")
            print 'Generating a new log file.'