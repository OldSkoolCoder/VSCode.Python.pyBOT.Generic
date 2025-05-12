from ast import Mod
import socket
# Only Uncomment if running on a raspberry Pi
#import board
import ssl
import json
import datetime
import time

from collections import namedtuple
from GlobalFunctions import *
import config
import ChatPoints
import Moderators
import ChannelData
import MasterMind
import Voting
import ShoutOuts
import SoundFx
import Sounds
import requests
import Poll

# Only Uncomment if running on a raspberry Pi
# import Matrix
import NeoPixels


Message = namedtuple(
    'Message',
    'prefix user channel ircCommand ircArgs text textCommand textArgs'
)

# Prefix            user              text
#               irc_command           text_command  text_args
#:tmi.twitch.tv 372 oldskoolcoderbot :You are in a maze of twisty passages, all alike.
#:tmi.twitch.tv 372 oldskoolcoderbot :!AddAMK       @OldSkoolCoder 10

# Username      Prefix                                    ircCommand Channel      Text
#:oldskoolcoder!oldskoolcoder@oldskoolcoder.tmi.twitch.tv PRIVMSG #oldskoolcoder :ello

#Sample Cheer Message
#Message(prefix='mikroman3526!mikroman3526@mikroman3526.tmi.twitch.tv', user='mikroman3526', channel='oldskoolcoder', ircCommand='PRIVMSG', ircArgs=['#oldskoolcoder'], text='Cheer100', textCommand=None, textArgs=None)

class TwitchBOT:
    def __init__(self, sio):
        self.sio = sio
        self.ircServer = config.TWITCHSERVER
        self.ircPort = config.TWITCHPORT         # SSL Port
        self.oAuthToken = config.OAUTH_TOKEN
        self.userName = config.USERNAME
        self.channels = config.CHANNELS
        self.commandPrefix = '!'
        self.staticCommands = {}
        self.staticCommandsFilename = config.DEFAULT_JSON_DIRECTORY + 'Commands.json'
        self.staticCommandsSchema = {
            "templateCommands": {},
            "descriptionCommands": {},
            "adminCommands": {},
        }
        self.points = ChatPoints.ChatPoints()
        self.moderators = Moderators.Moderators()
        self.channelData = ChannelData.ChannelData()

# Only Uncomment if running on a raspberry Pi
        # self.Matrix = Matrix.Matrix(4,0,8)
        self.NeoPixels = NeoPixels.NeoPixels()

        self.CodeBreaker = MasterMind.MasterMind(self.sio)
        self.Voting = Voting.Voting(self.sio)

        self.ShoutOuts = ShoutOuts.ShoutOuts()

        self.Listen = SoundFx.SoundFx("Listen.json")
        self.listenLastUsed = datetime.datetime(2022,1,1,0,0,0)

        self.Intros = SoundFx.SoundFx("Intro.json")
        self.Planks = SoundFx.SoundFx("Plank.json")
        self.Sounds = Sounds.Sounds()
        self.Poll = Poll.Poll(self.sio)

        self.customCommands = {
            'addpoints': self.processAddPoints,
            'subpoints': self.processSubPoints,
            'mypoints': self.processMyPoints,
            'top10': self.processTop10Points,
            'help': self.processListCommand,
            'mymods': self.processMyMods,
            'addmod': self.processAddMod,
            'removemod': self.processRemoveMod,
            'addban': self.processAddBan,
            'removeban': self.processRemoveBan,
            'mybans': self.processMyBans,
            'msg': self.processMsgCommand,
            'background': self.processPlasmaCommand,
            'backcolour': self.processBackColourCommand,
            'title': self.processTitleCommand,
            'newsub': self.processNewSubscriber,
            'newfollow': self.processNewFollower,
            'newcheer': self.processNewCheer,
            'listen': self.processListenCommand,
            'init': self.processInitCommand,
            'startgame': self.processStartGame,
            'guess': self.processGuess,
            'startvote': self.processStartVoting,
            'vote': self.processVote,
            'closevote': self.processCloseVoting,
            'addstreamer': self.processAddStreamer,
            'addlisten': self.processAddListen,
            'dellisten': self.processDelListen,
            'intro': self.processIntroCommand,
            'addintro': self.processAddIntro,
            'delintro': self.processDelIntro,
            'plank': self.processPlankCommand,
            'addplank': self.processAddPlank,
            'delplank': self.processDelPlank,
            'play': self.processPlayCommand,
            'addplay': self.processAddPlay,
            'delplay': self.processDelPlay,
            'clock': self.processClock,
            'fruit': self.processSlots,
            'shoutouts': self.processShoutOuts,
            'startpoll': self.processStartPoll,
            'poll': self.processPoll,
            'closepoll': self.processClosePoll,

# Only Uncomment if running on a raspberry Pi
            # 'neocolour': self.processNeoColour,
        }

    #-------------------------------------------------------------------------------------------------------------------------------
    def init(self):
        self.readStaticCommands()
        self.points.readPoints()
        self.moderators.readMods()
        self.channelData.readChannelData()
        self.channelData.grabChannelData(self.sio)

        self.CodeBreaker.readMasterMind()
        self.Voting.readVotes()
        self.ShoutOuts.readShoutOuts()
        self.ShoutOuts.resetShoutOuts()
        self.Listen.readSoundFx()
        self.Intros.readSoundFx()
        self.Planks.readSoundFx()
        self.Sounds.readSounds()
        self.Poll.readPolls()

        self.NeoPixels.readHTMLColours()

        traceFile = open("traceFile.txt", "w")
        traceFile.close()

        self.connect()

    #-------------------------------------------------------------------------------------------------------------------------------
    def connect(self):
        self.irc = ssl.wrap_socket(socket.socket())
        self.irc.connect((self.ircServer, self.ircPort))
        self.sendCommand(f'PASS {self.oAuthToken}')
        self.sendCommand(f'NICK {self.userName}')
        for channel in self.channels:
            self.sendCommand(f'JOIN #{channel}')
            self.sendPrivmsg(channel, f'Hey there, The new Python {config.VERSION}BOT vsn {config.VERSIONNUMBER} is now online ', '')
            databaseEntries = len(self.points.Points['entries'])
            self.sendPrivmsg(channel, f'The Database is now online and {databaseEntries} entries have been detected..', '')
        self.loopForMessages()

    #-------------------------------------------------------------------------------------------------------------------------------
    def sendCommand(self, command):
        if 'PASS' not in command:
            print (f'< {command}')
        self.irc.send((command + '\r\n').encode())

    #-------------------------------------------------------------------------------------------------------------------------------
    def sendPrivmsg(self, channel, text, state=''):

        text = f'PRIVMSG #{channel} :{text}'
        if state == "ERROR":
            if config.ERR_DESTINATION == config.ERR_CONSOLE:
                print(text)
            else:
                self.sendCommand(text)
        else:
            self.sendCommand(text)

    #-------------------------------------------------------------------------------------------------------------------------------
    def sendWhispermsg(self, channel, user, text, state):

        text = f'PRIVMSG {channel} :/w {user} {text}'
        if state == "ERROR":
            if config.ERR_DESTINATION == config.ERR_CONSOLE:
                print(text)
            else:
                self.sendCommand(text)
        else:
            self.sendCommand(text)

    #-------------------------------------------------------------------------------------------------------------------------------
    def loopForMessages(self):
        while True:
            receivedMsgs = self.irc.recv(2048).decode()
            for receivedMsg in receivedMsgs.split('\r\n'):
                self.handleMessage(receivedMsg)

    #-------------------------------------------------------------------------------------------------------------------------------
    def handleMessage(self, receivedMsg):
        if len(receivedMsg) == 0:
            return

        traceFile = open("traceFile.txt", "a")
        traceFile.write(f'> {receivedMsg} ----')
        #print(f'> {receivedMsg}')
        message = self.parseMessage(receivedMsg)
        traceFile.write(f'> {message}\r\n')
        traceFile.close()
        print(f'> {message}')

        if message.ircCommand == 'PING':
            self.sendCommand(f'PONG :{config.TWITCH_TMI_SERVER}')

        if message.ircCommand == 'PRIVMSG':
            if self.ShoutOuts.isStreamer(message.user) == True:
                text = f"!so @{message.user}"
                self.sendPrivmsg(message.channel, text, '') 

                customSFxFile = self.Intros.isStreamer(message.user)
                if customSFxFile != "":
                    SFxFile = customSFxFile
                    self.sio.call('listen', config.SFX_DIRECTORY + SFxFile + config.SFX_EXTENSION)

            if message.user.lower() not in ['streamlabs', config.USERNAME.lower()]:
                self.sio.call('chatmsg', [message.user.upper(), message.text])
                
            if self.moderators.isBanned(message.user) == False:
                try:
                    if config.USERS_NOT_GAIN_POINTS.index(message.user.upper()):
                        pass
                except:
                    self.points.addPoints(message.user, config.POINTS_PER_CHAT_LINE)

                if message.textCommand in self.customCommands:
                    self.customCommands[message.textCommand](message)
                elif message.textCommand in self.staticCommands['templateCommands']:
                    self.handleStaticCommand(
                        message,
                        message.textCommand,
                        self.staticCommands['templateCommands'][message.textCommand]
                    )
            elif message.textCommand != None:
                text = f"Sorry @{message.user}, Your not authorised to use any of my commands!"
                self.sendPrivmsg(message.channel, text, '') 


    #-------------------------------------------------------------------------------------------------------------------------------
    def handleStaticCommand(self, message, textCommand, commandTemplate):
        try:
            text = commandTemplate.format(**{'message' : message}) 
            self.sendPrivmsg(message.channel, text, '') 
        except IndexError:
            text = f"@{message.user} Your command is missing some arugments!"
            self.sendPrivmsg(message.channel, text, '') 
        except Exception as e:
            print('Error while handling static commands.', message, commandTemplate)
            print(e)

    #-------------------------------------------------------------------------------------------------------------------------------
    def parseMessage(self, messageReceived):
        messageParts = messageReceived.split(' ')

        prefix = None
        user = None
        channel = None
        text = None
        textCommand = None
        textArgs = None
        ircCommand = None
        ircArgs = None

        # Grab Prefix and User if the line starts with a ':'
        if messageParts[0].startswith(':'):
            prefix = removePrefix(messageParts[0],':')
            user = self.getUserFromPrefix(prefix)
            messageParts = messageParts[1:]

        textStart = next((idx for idx, part in enumerate(messageParts) if part.startswith(':')), None)

        if textStart is not None:
            textParts = messageParts[textStart:]
            textParts[0] = textParts[0][1:]
            text = ' '.join(textParts)

            if textParts[0].startswith(self.commandPrefix):
                textCommand = removePrefix(textParts[0], self.commandPrefix)
                textArgs = textParts[1:]

            messageParts = messageParts[:textStart]

        ircCommand = messageParts[0]
        ircArgs = messageParts[1:]

        hashStart = next((idx for idx, part in enumerate(ircArgs) if part.startswith('#')), None)

        if hashStart is not None:
            channel = ircArgs[hashStart][1:]

        message = Message(
            prefix = prefix,
            user = user,
            channel = channel,
            text = text,
            textCommand = textCommand,
            textArgs = textArgs,
            ircCommand = ircCommand,
            ircArgs = ircArgs,
        )
        return message

    #-------------------------------------------------------------------------------------------------------------------------------
    def getUserFromPrefix(self, prefix):
        domain = prefix.split('!')[0]

        if domain.endswith(f'.{config.TWITCH_TMI_SERVER}'):
            return domain.replace(f'.{config.TWITCH_TMI_SERVER}','')

        if config.TWITCH_TMI_SERVER not in domain:
            return domain # Username

        return None

    #-------------------------------------------------------------------------------------------------------------------------------
    def readStaticCommands(self):
        with open(self.staticCommandsFilename, 'r') as file:
            self.staticCommands = json.load(file)
            isSchemaClean = self.ensureStaticCommandSchema()
            if not isSchemaClean:
                self.writeStaticCommands()

    #-------------------------------------------------------------------------------------------------------------------------------
    def writeStaticCommands(self):
        with open(self.staticCommandsFilename, 'w') as file:
            json.dump(self.staticCommandsFilename, file,sort_keys=False,indent=2)

    #-------------------------------------------------------------------------------------------------------------------------------
    def ensureStaticCommandSchema(self):
        isClean = True

        for key in self.staticCommandsSchema:
            if key not in self.staticCommands:
                isClean = False
                self.staticCommands[key] = self.staticCommandsSchema[key]
        return isClean

    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddPoints(self, message):
        msgToSend = self.points.processAddPoints(message, self.moderators.isAllowedToExecute(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processSubPoints(self, message):
        msgToSend = self.points.processSubPoints(message, self.moderators.isAllowedToExecute(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processMyPoints(self, message):
        msgToSend = self.points.processMyPoints(message)
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processTop10Points(self, message):
        self.points.processTop10Points(message, self)

    #-------------------------------------------------------------------------------------------------------------------------------
    def processListCommand(self, message):
        template_cmd_names = list(self.staticCommands['descriptionCommands'])
        print(template_cmd_names)
        for cmd in template_cmd_names:
            text = self.staticCommands['descriptionCommands'][cmd]
            strCommand = self.commandPrefix + cmd + " : " + text
            self.sendPrivmsg(message.channel, strCommand, '')

        strCommand = ""
        if self.moderators.isAdmin(message) or self.moderators.isAllowedToExecute(message):
            template_cmd_names = list(self.staticCommands['adminCommands'])
            print(template_cmd_names)
            for cmd in template_cmd_names:
                text = self.staticCommands['adminCommands'][cmd]
                strCommand = self.commandPrefix + cmd + " : " + text
                self.sendPrivmsg(message.channel, strCommand, '')


    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddMod(self,message):
        msgToSend = self.moderators.processAddMod(message, self.moderators.isAdmin(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processRemoveMod(self,message):
        msgToSend = self.moderators.processRemoveMod(message, self.moderators.isAdmin(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processMyMods(self,message):
        msgToSend = self.moderators.processMyMods(message, self.moderators.isAdmin(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddBan(self,message):
        msgToSend = self.moderators.processAddBan(message, self.moderators.isAdmin(message), self.moderators.isAllowedToExecute(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processRemoveBan(self,message):
        msgToSend = self.moderators.processRemoveBan(message, self.moderators.isAdmin(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processMyBans(self,message):
        msgToSend = self.moderators.processMyBans(message, self.moderators.isAdmin(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processMsgCommand(self, message):
        if len(message.textArgs) < 1 or len(' '.join(message.textArgs)) > config.MESSAGE_MAX_LENGTH :
            text = f'@{message.user} Usage: !msg <text> (up to {config.MESSAGE_MAX_LENGTH} chars)'
            self.sendPrivmsg(message.channel, text, 'ERROR') 
            return
# Only Uncomment if running on a raspberry Pi
#        self.Matrix.showMsg(' '.join(message.textArgs))
        self.sio.call('msg', ' '.join(message.textArgs))

    #-------------------------------------------------------------------------------------------------------------------------------
    def processPlasmaCommand(self, message):
        # !background <theme> plasma
        if len(message.textArgs) < 1:
            text = f'@{message.user} Usage: !background <theme>'
            self.sendPrivmsg(message.channel, text, 'ERROR') 
            return
        self.sio.call('plasma', ' '.join(message.textArgs))

    #-------------------------------------------------------------------------------------------------------------------------------
    def processBackColourCommand(self, message):
        if len(message.textArgs) < 1:
            text = f'@{message.user} Usage: !backcolour <colour>'
            self.sendPrivmsg(message.channel, text, '') 
            return
        print(message.textArgs)
        RGB = self.NeoPixels.getHTMLColourRGB(message.textArgs[0])
        #self.sio.call('backcolour', ' '.join(message.textArgs))
        self.sio.call('backcolour', ' '.join(["#" + RGB]))
# Only Uncomment if running on a raspberry Pi
        # self.NeoPixels.changeColour(RGB)

    #-------------------------------------------------------------------------------------------------------------------------------
    def processTitleCommand(self,message):
        if self.moderators.isAdmin(message):
            self.sio.call('title', ' '.join(message.textArgs))
            
        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
            self.sendPrivmsg(message.channel, text, 'ERROR')             

    #-------------------------------------------------------------------------------------------------------------------------------
    def processNewSubscriber(self, message):
        if self.moderators.isAllowedToExecute(message):
            user = ''
            noOfMonths = 0

            if len(message.textArgs) < 2:
                text = f'@{message.user} Usage: !newsub <user> <months>'
                self.sendPrivmsg(message.channel, text, 'ERROR') 
                return
            
            try:
                user = message.textArgs[0].replace('@','')
                
                noOfMonths = int(message.textArgs[1])
            except IndexError:
                noOfMonths = 0

            except Exception as e:
                print('Error while handling static commands.', message)
                print(e)

            finally:
                self.sendPrivmsg(message.channel, f'{user}, has subscribed for {noOfMonths} months now', '')
                data = [user,noOfMonths]
                self.channelData.addSub(user,noOfMonths)
                self.sio.call('sub', data)

        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
            self.sendPrivmsg(message.channel, text, 'ERROR') 

    #-------------------------------------------------------------------------------------------------------------------------------
    def processNewFollower(self, message):
        if self.moderators.isAllowedToExecute(message):
            user = ''

            if len(message.textArgs) < 2:
                text = f'@{message.user} Usage: !newfollow <user>'
                self.sendPrivmsg(message.channel, text, 'ERROR') 
                return
            user = message.textArgs[0].replace('@','')
            
            self.sendPrivmsg(message.channel, f'{user}, has just followed us, please welcome them', '')
            data = [user]
            self.channelData.addFollow(user)
            self.sio.call('follow', data)

        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
            self.sendPrivmsg(message.channel, text, 'ERROR') 

    #-------------------------------------------------------------------------------------------------------------------------------
    def processNewCheer(self, message):
        if self.moderators.isAllowedToExecute(message):
            user = ''
            noOfBits = 0

            if len(message.textArgs) < 2:
                text = f'@{message.user} Usage: !newcheer <user> <bits>'
                self.sendPrivmsg(message.channel, text, 'ERROR') 
                return

            try:
                user = message.textArgs[0].replace('@','')
                
                noOfBits = int(message.textArgs[1])
            except IndexError:
                noOfBits = 0

            except Exception as e:
                print('Error while handling static commands.', message)
                print(e)

            finally:
                if noOfBits == 1:
                    self.sendPrivmsg(message.channel, f'{user}, Thank you for the {noOfBits} Bit, Bah Humbug.... lol', '')
                else:
                    self.sendPrivmsg(message.channel, f'{user}, Thank you for the {noOfBits} Bits', '')
                data = [user,noOfBits]
                self.channelData.addCheer(user, noOfBits)
                self.sio.call('cheer', data)

        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
            self.sendPrivmsg(message.channel, text, 'ERROR') 

    #-------------------------------------------------------------------------------------------------------------------------------
    def processListenCommand(self, message):
        msgToSend = self.Listen.processCommand(message, self.moderators.isAdmin(message), self.sio, config.DEFAULTLISTENFILENAME)
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processInitCommand(self, message):
        if self.moderators.isAdmin(message):
            self.channelData.grabChannelData(self.sio)

            text = f"@{message.user}, BOT has been reset, you are good to GO!!!!"
            self.sendPrivmsg(message.channel, text, '')            

        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
            self.sendPrivmsg(message.channel, text, 'ERROR')             

    #-------------------------------------------------------------------------------------------------------------------------------
    def processStartGame(self, message):
        msgToSend = self.CodeBreaker.processStartGame(message, self.moderators.isAdmin(message), self.moderators.isAllowedToExecute(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processGuess(self, message):
        msgToSend = self.CodeBreaker.processGuess(message)
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processStartVoting(self, message):
        msgToSend = self.Voting.processStartVoting(message, self.moderators.isAdmin(message), self.moderators.isAllowedToExecute(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processVote(self, message):
        msgToSend = self.Voting.processVote(message)
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processCloseVoting(self, message):
        msgToSend = self.Voting.processCloseVoting(message, self.moderators.isAdmin(message), self.moderators.isAllowedToExecute(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddStreamer(self, message):
        msgToSend = self.ShoutOuts.processAddStreamer(message, self.moderators.isAdmin(message), self.moderators.isAllowedToExecute(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

#-------------------------------------------------------------------------------------------------------------------------------
    def processShoutOuts(self, message):
        msgToSend = self.ShoutOuts.processShoutOuts(message, self, self.moderators.isMod(message), self.moderators.isAdmin(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processNeoColour(self, message):

        rgbColour = ''

        rgbColour = message.textArgs[0].replace('#','')
        if len(rgbColour) < 1:
            text = f'@{message.user} Usage: !neoColour <HTML Colour>'
            self.sendPrivmsg(message.channel, text, '') 
            return

# Only Uncomment if running on a raspberry Pi
        # self.NeoPixels.changeColour(rgbColour)

        # if Added == True:
        #     text = f"@{message.user}, This streamer has been added."
        #     print(text)
        # else:
        #     text = f"@{message.user}, Sorry, This streamer already exists."
        #     print(text)

        # self.sendPrivmsg(message.channel, text, '') 
        # self.sendPrivmsg(message.channel, text, '')             

    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddSoundFx(self, message, SoundFxName, SoundFxObject):
        msgToSend = SoundFxObject.processAddSoundFx(message, SoundFxName, self.moderators.isAdmin(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processDelSoundFx(self, message, SoundFxName, SoundFxObject):
        msgToSend = SoundFxObject.processDelSoundFx(message, SoundFxName, self.moderators.isAdmin(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddListen(self, message):
        self.processAddSoundFx(message, "Listen", self.Listen)

    #-------------------------------------------------------------------------------------------------------------------------------
    def processDelListen(self, message):
        self.processDelSoundFx(message, "Listen", self.Listen)

    #-------------------------------------------------------------------------------------------------------------------------------
    def processIntroCommand(self, message):
        msgToSend = self.Intros.processCommand(message, self.moderators.isAdmin(message), self.sio)
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddIntro(self, message):
        self.processAddSoundFx(message, "Intro", self.Intros)

    #-------------------------------------------------------------------------------------------------------------------------------
    def processDelIntro(self, message):
        self.processDelSoundFx(message, "Intro", self.Intros)

    #-------------------------------------------------------------------------------------------------------------------------------
    def processPlankCommand(self, message):
        msgToSend = self.Planks.processCommand(message, self.moderators.isAdmin(message), self.sio)
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddPlank(self, message):
        self.processAddSoundFx(message, "Plank", self.Planks)

    #-------------------------------------------------------------------------------------------------------------------------------
    def processDelPlank(self, message):
        self.processDelSoundFx(message, "Plank", self.Planks)

    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddPlay(self, message):
        msgToSend = self.Sounds.processAddPlay(message, self.moderators.isAdmin(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processDelPlay(self, message):
        msgToSend = self.Sounds.processDelPlay(message, self.moderators.isAdmin(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processPlayCommand(self, message):
        msgToSend = self.Sounds.processPlayCommand(message, self.moderators.isAdmin(message), self.sio)
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processClock(self, message):

        clocks = ['ANALOG','PONG','TETRIS']
        
        if len(message.textArgs) > 0:
            clockName = message.textArgs[0].replace('@','').upper()

            try:
                clockID = clocks.index(clockName)
                print(config.PANELSERVER + f'myClock?ClockMode={clockID}')

                try:
                    x = requests.get(config.PANELSERVER + f'myClock?ClockMode={clockID}')
                except:
                    pass

            except:
                self.sendPrivmsg(message.channel, 'That Clock Does not exist')

        else:
            clockNames = [
                '' + clockName
                for clockName in clocks
            ]

            self.sendPrivmsg(message.channel, 'Available clocks : ' + ', '.join(clockNames), '')


    #-------------------------------------------------------------------------------------------------------------------------------
    def processSlots(self, message):

        coolDownSecs = timeDifferenceInSeconds(self.listenLastUsed, datetime.datetime.now())

        if coolDownSecs >= config.SLOTS_COOLDOWN_TIME_SECS:
            try:
                bet = int(message.textArgs[0])
                if bet > 9999:
                    self.sendPrivmsg(message.channel, f'{message.user}, really, you trying to blow me up :p', 'ERROR')
                else:
                    if bet <=0:
                        self.sendPrivmsg(message.channel, f'{message.user}, really, negative or zero points.... whats the point in that :p', 'ERROR')
                    else:
                        points = self.points.myPoints(message.user)
                        if points > bet:
                            try:
                                self.points.subPoints(message.user, bet)
                                x = requests.get(config.PANELSERVER + f'mySlots?userName={message.user}&userPoints={points}&userBet={bet}')
                            except:
                                pass

                        else:
                            self.sendPrivmsg(message.channel, f'@{message.user}, does not have enough points', '')
            except IndexError:
                text = f"@{message.user} Your command is missing some arguments!"
                self.sendPrivmsg(message.channel, text, 'ERROR') 
            except Exception as e:
                print('Error while handling static commands.', message)
                print(e)
        else:
            self.sendPrivmsg(message.channel, f'{message.user} Cool down time has not elapsed, you have {config.SLOTS_COOLDOWN_TIME_SECS - coolDownSecs} Seconds left', 'ERROR')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processStartPoll(self, message):
        msgToSend = self.Poll.processStartPoll(message, self.moderators.isAdmin(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processPoll(self, message):
        msgToSend = self.Poll.processPoll(message, self.moderators.isAdmin(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processClosePoll(self, message):
        msgToSend = self.Poll.processClosePoll(message, self.moderators.isAdmin(message))
        if msgToSend != "":
            self.sendPrivmsg(message.channel, msgToSend, '')
