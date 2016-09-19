from connection import Connection

server = ('irc.rizon.no', 6697)
nick = 'Bubble'
password = 'password'

counter = 0
while counter != 5:
    counter += 1
    rizon = Connection(server, nick, password)
    rizon.connect_server()
    rizon.join_channel('#bubbletest')
    rizon.start()