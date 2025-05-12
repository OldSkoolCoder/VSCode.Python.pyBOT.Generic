import json
import config
import datetime
from GlobalFunctions import *

class Sounds:
    def __init__(self):
        self.Sounds = {}
        self.SoundsFilename = config.DEFAULT_JSON_DIRECTORY + 'Sounds.json'
        self.SoundsSchema= {
            "entries": 
                {}
        }
        self.listenLastUsed = datetime.datetime.now()

    #-------------------------------------------------------------------------------------------------------------------------------
    def readSounds(self):
        with open(self.SoundsFilename, 'r') as file:
            self.Sounds = json.load(file)
            isSchemaClean = ensureJSONSchema(self.SoundsSchema, self.Sounds)
            if not isSchemaClean:
                self.writeSounds()

    #-------------------------------------------------------------------------------------------------------------------------------
    def writeSounds(self):
        with open(self.SoundsFilename, 'w') as file:
            json.dump(self.Sounds, file,sort_keys=False,indent=2)

    #-------------------------------------------------------------------------------------------------------------------------------
    def addTo(self, SoundName, SoundsFileName):
        SoundName = SoundName.upper()
        SoundsFileName = SoundsFileName.upper()
        isAdded = False
        if SoundName not in self.Sounds['entries']:
            self.Sounds['entries'][SoundName] = SoundsFileName
            isAdded = True

        self.writeSounds()

        return isAdded

    #-------------------------------------------------------------------------------------------------------------------------------
    def delFrom(self, SoundName):
        SoundName = SoundName.upper()
        isRemoved = False
        if SoundName in self.Sounds['entries']:
            self.Sounds['entries'].pop(SoundName)
            isRemoved = True

        self.writeSounds()

        return isRemoved

    #-------------------------------------------------------------------------------------------------------------------------------
    def isSound(self, SoundName):
        SoundName = SoundName.upper()

        SoundsFileName = ""
        if SoundName in self.Sounds['entries']:
            SoundsFileName = self.Sounds['entries'][SoundName]

        return SoundsFileName

    #-------------------------------------------------------------------------------------------------------------------------------
    def listSounds(self):

        if len(self.Sounds['entries']) != 0:
            SoundNames = [
                '' + soundName
                for soundName in self.Sounds['entries']
            ]

            return 'Available sounds : ' + ', '.join(SoundNames)

        else:
            return 'No Sounds Available'

    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddPlay(self, message, IsAdmin):
        if IsAdmin:
            soundName = ''

            soundName = message.textArgs[0].replace('@','')
            if len(soundName) < 1:
                text = f'@{message.user} Usage: !addPlay <SoundName> <file.mp3>'

            Added = self.Sounds.addTo(soundName, message.textArgs[1])

            if Added == True:
                text = f"@{message.user}, This Sound has been added."
                print(text)
            else:
                text = f"@{message.user}, Sorry, This Sound already exists."
                print(text)

        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
            print(text)

        return text

    #-------------------------------------------------------------------------------------------------------------------------------
    def processDelPlay(self, message, IsAdmin):
        if IsAdmin:
            soundName = ''

            soundName = message.textArgs[0].replace('@','')
            if len(soundName) < 1:
                text = f'@{message.user} Usage: !delplay <SoundName>'

            Removed = self.Sounds.delFrom(soundName)

            if Removed == True:
                text = f"@{message.user}, This Sound has been removed."
                print(text)
            else:
                text = f"@{message.user}, Sorry, This Sound does not exist."
                print(text)

        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
            print(text)

        return text

    #-------------------------------------------------------------------------------------------------------------------------------
    def processPlayCommand(self, message, IsAdmin, sio):
        coolDownSecs = timeDifferenceInSeconds(self.listenLastUsed, datetime.datetime.now())

        if coolDownSecs >= config.LISTEN_COOLDOWN_TIME_SECS or IsAdmin:
            SoundName = ''
            if len(message.textArgs) > 0:
                SoundName = message.textArgs[0].replace('@','').upper()

                sfxFileName = ''
                customSFxFileName = self.Sounds.isSound(SoundName)
                if customSFxFileName != "":
                    sfxFileName = customSFxFileName

                sio.call('listen', config.SFX_DIRECTORY + sfxFileName + config.SFX_EXTENSION)
                self.listenLastUsed = datetime.datetime.now()

            else:
                text = self.Sounds.listSounds()

        else:
            text = f'{message.user} Cool down time has not elapsed, you have {config.LISTEN_COOLDOWN_TIME_SECS - coolDownSecs} Seconds left'

        return text



