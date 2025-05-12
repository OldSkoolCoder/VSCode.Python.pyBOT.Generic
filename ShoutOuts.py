import json
import config
import time

from GlobalFunctions import *

class ShoutOuts:
    def __init__(self):
        self.ShoutOuts = {}
        self.ShoutOutFilename = config.DEFAULT_JSON_DIRECTORY + 'ShoutOuts.json'
        self.ShoutOutSchema= {
            "entries": 
                {}
        }

    #-------------------------------------------------------------------------------------------------------------------------------
    def readShoutOuts(self):
        with open(self.ShoutOutFilename, 'r') as file:
            self.ShoutOuts = json.load(file)
            isSchemaClean = ensureJSONSchema(self.ShoutOutSchema, self.ShoutOuts)
            if not isSchemaClean:
                self.writeShoutOuts()

    #-------------------------------------------------------------------------------------------------------------------------------
    def writeShoutOuts(self):
        with open(self.ShoutOutFilename, 'w') as file:
            json.dump(self.ShoutOuts, file,sort_keys=False,indent=2)

    #-------------------------------------------------------------------------------------------------------------------------------
    def addStreamer(self, StreamerUserName):
        StreamerUserName = StreamerUserName.upper()
        isAdded = False
        if StreamerUserName not in self.ShoutOuts['entries']:
            self.ShoutOuts['entries'][StreamerUserName] = "N"
            isAdded = True

        self.writeShoutOuts()

        return isAdded

    #-------------------------------------------------------------------------------------------------------------------------------
    def isStreamer(self, StreamerUserName):
        StreamerUserName = StreamerUserName.upper()

        isFirstChat = False
        if StreamerUserName in self.ShoutOuts['entries']:
            if self.ShoutOuts['entries'][StreamerUserName] == "N":
                self.ShoutOuts['entries'][StreamerUserName] = "Y"
                isFirstChat = True

        self.writeShoutOuts()

        return isFirstChat

    #-------------------------------------------------------------------------------------------------------------------------------
    def resetShoutOuts(self):

        for StreamerUserName in self.ShoutOuts['entries']:
            self.ShoutOuts['entries'][StreamerUserName] = "N"

        self.writeShoutOuts()

    #-------------------------------------------------------------------------------------------------------------------------------
    def shoutOutStreamer(self):

        return self.ShoutOuts['entries'].items()

#-------------------------------------------------------------------------------------------------------------------------------
    def processShoutOuts(self, message, BOT, IsMod, IsAdmin):
        text = ""
        if IsMod or IsAdmin:
            sortedShoutOuts = self.shoutOutStreamer()

            for item in sortedShoutOuts:
                BOT.sendPrivmsg(message.channel, f'!so {item[0]}', '')
                time.sleep(2)

        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
            print(text)

        return text

    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddStreamer(self, message, IsAdmin, CanExecute):
        text = ""
        if IsAdmin or CanExecute:
            user = ''

            if len(message.textArgs) < 1:
                text = f'@{message.user} Usage: !addStreamer <user>'

            else:
                user = message.textArgs[0].replace('@','')
                Added = self.addStreamer(user)

                if Added == True:
                    text = f"@{message.user}, This streamer has been added."
                    print(text)
                else:
                    text = f"@{message.user}, Sorry, This streamer already exists."
                    print(text)

        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
            print(text)

        return text


