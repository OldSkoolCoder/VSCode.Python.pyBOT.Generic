import json
import config
import datetime
from GlobalFunctions import *

class SoundFx:
    def __init__(self, jsonFileName):
        self.SoundFx = {}
        self.SoundFxFilename = config.DEFAULT_JSON_DIRECTORY + jsonFileName
        self.SoundFxchema= {
            "entries": 
                {}
        }
        self.listenLastUsed = datetime.datetime.now()

    #-------------------------------------------------------------------------------------------------------------------------------
    def readSoundFx(self):
        with open(self.SoundFxFilename, 'r') as file:
            self.SoundFx = json.load(file)
            isSchemaClean = ensureJSONSchema(self.SoundFxchema, self.SoundFx)
            if not isSchemaClean:
                self.writeSoundFx()

    #-------------------------------------------------------------------------------------------------------------------------------
    def writeSoundFx(self):
        with open(self.SoundFxFilename, 'w') as file:
            json.dump(self.SoundFx, file,sort_keys=False,indent=2)

    #-------------------------------------------------------------------------------------------------------------------------------
    def addTo(self, TwitchUserName, SoundFxFileName):
        TwitchUserName = TwitchUserName.upper()
        SoundFxFileName = SoundFxFileName.upper()
        isAdded = False
        if TwitchUserName not in self.SoundFx['entries']:
            self.SoundFx['entries'][TwitchUserName] = SoundFxFileName
            isAdded = True

        self.writeSoundFx()

        return isAdded

    #-------------------------------------------------------------------------------------------------------------------------------
    def delFrom(self, TwitchUserName):
        TwitchUserName = TwitchUserName.upper()
        isRemoved = False
        if TwitchUserName in self.SoundFx['entries']:
            self.SoundFx['entries'].pop(TwitchUserName)
            isRemoved = True

        self.writeSoundFx()

        return isRemoved

    #-------------------------------------------------------------------------------------------------------------------------------
    def isStreamer(self, TwitchUserName):
        TwitchUserName = TwitchUserName.upper()

        SoundFxFileName = ""
        if TwitchUserName in self.SoundFx['entries']:
            SoundFxFileName = self.SoundFx['entries'][TwitchUserName]

        return SoundFxFileName

    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddSoundFx(self, message, SoundFxName, IsAdmin):
        if IsAdmin:
            user = ''

            if len(message.textArgs) < 1:
                text = f'@{message.user} Usage: !add{SoundFxName} <user> <file.mp3>'

            else:
                user = message.textArgs[0].replace('@','')
                Added = self.addTo(user, message.textArgs[1])

                if Added == True:
                    text = f"@{message.user}, This Twitcher has been added."
                    print(text)
                else:
                    text = f"@{message.user}, Sorry, This Twitcher already exists."
                    print(text)

        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
            print(text)

        return text
    
    #-------------------------------------------------------------------------------------------------------------------------------
    def processDelSoundFx(self, message, SoundFxName, SoundFxObject, IsAdmin):
        if IsAdmin:
            user = ''

            if len(message.textArgs) < 1:
                text = f'@{message.user} Usage: !del{SoundFxName} <user>'

            else:
                user = message.textArgs[0].replace('@','')
                Removed = SoundFxObject.delFrom(user)

                if Removed == True:
                    text = f"@{message.user}, This Twitcher has been removed."
                    print(text)
                else:
                    text = f"@{message.user}, Sorry, This Twitcher does not already exists."
                    print(text)

        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
            print(text)

        return text

    #-------------------------------------------------------------------------------------------------------------------------------
    def processCommand(self, message, IsAdmin, sio, defaultSFX=''):
        coolDownSecs = timeDifferenceInSeconds(self.listenLastUsed, datetime.datetime.now())

        if (coolDownSecs >= config.LISTEN_COOLDOWN_TIME_SECS) or IsAdmin:
            user = ''
            if IsAdmin and len(message.textArgs) > 0:
                user = message.textArgs[0].replace('@','').upper()
            else:
                user = message.user.replace('@','').upper()

            sfxFileName = defaultSFX
            customSFxFileName = self.isStreamer(user)
            if customSFxFileName != "":
                sfxFileName = customSFxFileName

            if sfxFileName != "":
                sio.call('listen', config.SFX_DIRECTORY + sfxFileName + config.SFX_EXTENSION)
                if defaultSFX != "":
                    sio.call('showimage', config.IMG_DIRECTORY + sfxFileName + config.IMG_EXTENSION)
                self.listenLastUsed = datetime.datetime.now()
            return ""
        else:
            return f'{message.user} Cool down time has not elapsed, you have {config.LISTEN_COOLDOWN_TIME_SECS - coolDownSecs} Seconds left'


