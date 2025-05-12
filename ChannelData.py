import json
from GlobalFunctions import *
import config

class ChannelData:
    def __init__(self):
        self.ChannelData = {}
        self.ChannelDataFilename = config.DEFAULT_JSON_DIRECTORY + 'ChannelData.json'
        self.ChannelDataSchema= {
            "latestSub":{"User":"", "Months":0},
            "latestFollow":{"User":""},
            "latestCheer":{"User":"", "Bits":0}
        }

    #-------------------------------------------------------------------------------------------------------------------------------
    def readChannelData(self):
        with open(self.ChannelDataFilename, 'r') as file:
            self.ChannelData = json.load(file)
            isSchemaClean = ensureJSONSchema(self.ChannelDataSchema, self.ChannelData)
            if not isSchemaClean:
                self.writeChannelData()

    #-------------------------------------------------------------------------------------------------------------------------------
    def writeChannelData(self):
        with open(self.ChannelDataFilename, 'w') as file:
            json.dump(self.ChannelData, file,sort_keys=False,indent=2)

    #-------------------------------------------------------------------------------------------------------------------------------
    def addSub(self, username, months):
        username = username.upper()
        self.ChannelData['latestSub']['User'] = username
        self.ChannelData['latestSub']['Months'] = months
        self.writeChannelData()

    #-------------------------------------------------------------------------------------------------------------------------------
    def addFollow(self, username):
        username = username.upper()
        self.ChannelData['latestFollow']['User'] = username
        self.writeChannelData()

    #-------------------------------------------------------------------------------------------------------------------------------
    def addCheer(self, username, bits):
        username = username.upper()
        self.ChannelData['latestCheer']['User'] = username
        self.ChannelData['latestCheer']['Bits'] = bits
        self.writeChannelData()

    #-------------------------------------------------------------------------------------------------------------------------------
    def grabChannelData(self, sio):
        data=[]
        data.append(self.ChannelData['latestSub']['User'])
        data.append(self.ChannelData['latestSub']['Months'])
        data.append(self.ChannelData['latestFollow']['User'])
        data.append(self.ChannelData['latestCheer']['User'])
        data.append(self.ChannelData['latestCheer']['Bits'])
        sio.call('init', data)
