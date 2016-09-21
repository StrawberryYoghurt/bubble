# Bubble
Bubble is a multi-purpose IRC bot, written in Python 2. The goal is to make her into a one size fits all, modular bot that's easy to use and adapt to your needs. The goal of this project is to create a robust bot with modules that range from channel functionalities like logging, memos and assistance with moderation to pen and paper RPG dice rolls and tracking. 

Right now, there is some basic functionality. Bubble can maintain a connection, log channels, and has a few simple commands. 

# Usage
To start Bubble, run start.py. Her settings can be changed in config.py. She'll automatically log all channels she's in, and will also maintain a raw logfile, containing all the lines she receives. You can send any IRC command in raw form by using a keyboard interrupt (CTRL+C) and typing in your message. 

# Commands
Bubble has just a few commands available at the moment. 

-"Hi Bubble" will make her politely respond. 

-"Hey Bubble" will return a string created by a Markov generator, using the logs of the channel the command was given in. 

-"!context" will return a pastebin link with the last 200 lines. (Not exactly 200 right now.)

-"!ex #" rolls the number of dice specified instead of #, returning the hits. It will also give the number of hits for a damage roll. Example: 

Yuki_: !ex 5 <Bubble> 

Yuki_: has rolled 5 dice. [6, 10, 5, 6, 8] 3 hits. Damage roll: 2

# To do

-Remove double text to make the raw logs human-readable - create one function to do that. Include bans, kicks, nick changes.

-Add op functionalities.

-Add a vote command, for democratic channels. 

-Add memo, lastseen commands.

# Contact
To talk to me, message Yuki_ on Freenode or Rizon.