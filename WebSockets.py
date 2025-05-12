#!/usr/bin/python3
import eventlet
import socketio
import config

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={'/': 'public/'})

@sio.event
def connect(sid, environment):
   print(f'SessionID : {sid} has Connected') 

@sio.event
def disconnect(sid):
   print(f'SessionID : {sid} has disconnected') 

@sio.event
def sum(sid, data):
    print(f'SessionID : {sid} has sent {data}') 
    result = data['numbers'][0] + data['numbers'][1]
    sio.emit('sumResult', {'result': result})

@sio.event
def msg(sid, data):
    sio.emit('msg', data)

@sio.event
def plasma(sid, data):
    sio.emit('plasma', data)

@sio.event
def backcolour(sid, data):
    sio.emit('backcolour', data)

@sio.event
def title(sid, data):
    sio.emit('title', data)

@sio.event
def init(sid, data):
    sio.emit('init', data)

@sio.event
def sub(sid, data):
    sio.emit('sub', data)

@sio.event
def follow(sid, data):
    sio.emit('follow', data)

@sio.event
def cheer(sid, data):
    sio.emit('cheer', data)

@sio.event
def listen(sid, data):
    sio.emit('listen', data)

@sio.event
def gamestart(sid, data):
    sio.emit('gamestart', data)

@sio.event
def gameupdate(sid, data):
    sio.emit('gameupdate', data)

@sio.event
def gameended(sid, data):
    sio.emit('gameended', data)

@sio.event
def showimage(sid, data):
    sio.emit('showimage', data)

@sio.event
def chatmsg(sid, data):
    sio.emit('chatmsg', data)

@sio.event
def pollstart(sid, data):
    sio.emit('pollstart', data)

@sio.event
def pollupdate(sid, data):
    sio.emit('pollupdate', data)

@sio.event
def pollended(sid, data):
    sio.emit('pollended', data)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', config.WEBSOCKETPORT)), app)