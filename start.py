from connection import Connection

password = False
for line in open('config.txt','r'):
    if line[:6] == "server":
       server = line[7:line.find('\r')]
    if line[:4] == "port":
       port = int(line[5:line.find('\r')])
    if line[:4] == "nick":
       nick = line[5:line.find('\r')]
    if line[:5] == "ident":
       ident = line[6:line.find('\r')]
    if line[:8] == "realname":
       realname = line[9:line.find('\r')]
    if line[:8] == "password":
       password = line[9:line.find('\r')]
    if line[:7] == "channel":
       channel = line[8:line.find('\r')]

counter = 0
while counter != 5:
    counter += 1
    connect = Connection(server, port, nick, ident, realname, password)
    connect.connect_server()
    connect.join_channel(channel)
    connect.start()