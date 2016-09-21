from connection import Connection
from config import *

counter = 0
while counter != 5:
    counter += 1
    connect = Connection(server, port, nick, ident, realname, password)
    connect.connect_server()
    connect.join_channel(channel)
    connect.start()