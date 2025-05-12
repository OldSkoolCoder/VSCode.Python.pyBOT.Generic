#!/usr/bin/python3
import TwitchBOT
import socketio
import config

sio = socketio.Client()

bot = TwitchBOT.TwitchBOT(sio)

@sio.event
def connect():
    print('client connect')

@sio.event
def disconnect():
    print('client disconnected')

if __name__ == '__main__':
    sio.connect(config.WEBSOCKETSERVER + ':' + str(config.WEBSOCKETPORT))
    bot.init()