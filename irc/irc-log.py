"""
Name             : Some Examples of Simple Python Script {BOT Log IRC}
Created By       : Agus Makmun (Summon Agus)
Blog             : bloggersmart.net - python.web.id
License          : GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
Documentation    : https://github.com/agusmakmun/Some-Examples-of-Simple-Python-Script/
"""

import socket
import sys, datetime

server = "irc.freenode.net"
channel = "#channel"
botnick = "bot-nickname"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
print "connecting to:"+server
irc.connect((server, 6667)) #connects to the server
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :This is a fun bot!\n") #user authentication
irc.send("NICK "+ botnick +"\n") #sets nick
irc.send("PRIVMSG nickserv :iNOOPE\r\n") #auth
irc.send("JOIN "+ channel +"\n") #join the chan

date = str(datetime.datetime.now()).split('.')[0]

import inspect
import logging, os
path = 'mypath/log-irc'

def function_logger(file_level, console_level = None):
    function_name = inspect.stack()[1][3]
    logger = logging.getLogger(function_name)
    logger.setLevel(logging.DEBUG) #By default, logs all messages

    if console_level != None:
        ch = logging.StreamHandler() #StreamHandler logs to console
        ch.setLevel(console_level)
        ch_format = logging.Formatter('%(asctime)s - %(message)s')
        ch.setFormatter(ch_format)
        logger.addHandler(ch)

    #fh = logging.FileHandler("{0}.log".format(function_name))
    fh = logging.FileHandler(os.path.join(path, str(datetime.datetime.now()).split()[0]+".log"))
    fh.setLevel(file_level)
    fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(fh_format)
    logger.addHandler(fh)

    return logger

def irc_log():
    log_logger = function_logger(logging.DEBUG, logging.ERROR)
    #log_logger.info('info message')
    
    while 1:#puts it in a loop
        text1 = irc.recv(2040)
        text = [date], text1
        
        try:
            spl = str(text).split()
            ip = spl[2].split("/")[-1]
            info = spl[3]
            user = spl[2].split("!")[0][2:]
            msg = str(text).split(channel)[-1][2:].replace("\\r\\n')", "")

            if info == 'JOIN':
                print date, "| <"+user+"> |", ip, "| has joined", channel
                log_logger.info("<"+user+"> | "+ip+" | has joined "+channel)
                
            elif info == 'QUIT':
                print date, "| <"+user+"> |", ip, "| was closed."
                log_logger.info("<"+user+"> | "+ip+" | was closed.")
                
            elif info == 'PART':
                print date, "| <"+user+"> |", ip, "| was left."
                log_logger.info("<"+user+"> | "+ip+" | was left.")
                
            elif info == 'PRIVMSG':
                print date, "| <"+user+"> |", ip, "| Message:", msg
                log_logger.info("<"+user+"> | "+ip+" | Message: "+msg)
                
            elif text1.find('PING') != -1:
                    irc.send('PONG ' + text1.split()[1] + '\r\n') #reconnect irc-bot
            else:
                pass
        except:
            pass
    
def main():
    irc_log()
    logging.shutdown()

main()
