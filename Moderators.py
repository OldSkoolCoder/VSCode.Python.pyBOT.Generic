import json
import config
from GlobalFunctions import *
import config

class Moderators:
    def __init__(self):
        self.Mods = {}
        self.ModsFilename = config.DEFAULT_JSON_DIRECTORY + 'Moderators.json'
        self.ModsSchema= {
            "moderators": [],
            "banned": []
        }

    #-------------------------------------------------------------------------------------------------------------------------------
    def readMods(self):
        with open(self.ModsFilename, 'r') as file:
            self.Mods = json.load(file)
            isSchemaClean = ensureJSONSchema(self.ModsSchema, self.Mods)
            if not isSchemaClean:
                self.writeMods()

    #-------------------------------------------------------------------------------------------------------------------------------
    def writeMods(self):
        with open(self.ModsFilename, 'w') as file:
            json.dump(self.Mods, file,sort_keys=False,indent=2)

    #-------------------------------------------------------------------------------------------------------------------------------
    def AddMod(self,username):
        username = username.upper()
        self.Mods['moderators'].append(username)
        self.writeMods()

    #-------------------------------------------------------------------------------------------------------------------------------
    def removeMod(self, username):
        username = username.upper()
        self.Mods['moderators'].remove(username)
        self.writeMods()

    #-------------------------------------------------------------------------------------------------------------------------------
    def myMods(self):
        allMods = [
            '@' + modUser
            for modUser in self.Mods['moderators']
        ]
        return 'My Mods are : ' + ' '.join(allMods)

    #-------------------------------------------------------------------------------------------------------------------------------
    def isMod(self, message):
        username = message.user.upper()

        if username in self.Mods['moderators']:
            return True
        else:
            return False


    #-------------------------------------------------------------------------------------------------------------------------------
    def isAdmin(self, message):
        user = message.user.upper()

        if config.ADMINUSER.upper() == user:
            return True
        else:
            return False

    #-------------------------------------------------------------------------------------------------------------------------------
    def isAllowedToExecute(self, message):
        return self.isAdmin(message) or self.isMod(message)

    #-------------------------------------------------------------------------------------------------------------------------------
    def AddBanned(self,username):
        username = username.upper()
        self.Mods['banned'].append(username)
        self.writeMods()

    #-------------------------------------------------------------------------------------------------------------------------------
    def removeBanned(self, username):
        username = username.upper()
        self.Mods['banned'].remove(username)
        self.writeMods()

    #-------------------------------------------------------------------------------------------------------------------------------
    def myBannedList(self):
        allBans = [
            '@' + bannedUser
            for bannedUser in self.Mods['banned']
        ]
        return 'My Banned List is : ' + ' '.join(allBans)

    #-------------------------------------------------------------------------------------------------------------------------------
    def isBanned(self,username):
        username = username.upper()

        if username in self.Mods['banned']:
            return True
        else:
            return False

    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddMod(self,message, IsAdmin):
        text =""
        if IsAdmin:
            user = ''
            try:
                user = message.textArgs[0].replace('@','')
                self.AddMod(user)
            
            except IndexError:
                print('No Arguments found for this command')
            except Exception as e:
                print('Error while handling static commands.', message)
                print(e)
            
        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"

        return text

    #-------------------------------------------------------------------------------------------------------------------------------
    def processRemoveMod(self,message, IsAdmin):
        text =""
        if IsAdmin:
            user = ''
            try:
                user = message.textArgs[0].replace('@','')
                self.removeMod(user)

            except IndexError:
                print('No Arguments found for this command')
            except Exception as e:
                print('Error while handling static commands.', message)
                print(e)
            
        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"

        return text

    #-------------------------------------------------------------------------------------------------------------------------------
    def processMyMods(self,message, IsAdmin):
        text =""
        if IsAdmin:
            text = self.myMods()
            
        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"

        return text

    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddBan(self,message, IsAdmin, CanExecute):
        text =""
        if IsAdmin or CanExecute:
            user = ''
            try:
                user = message.textArgs[0].replace('@','')
                self.AddBanned(user)
            
            except IndexError:
                print('No Arguments found for this command')
            except Exception as e:
                print('Error while handling static commands.', message)
                print(e)
            
        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"

        return text

    #-------------------------------------------------------------------------------------------------------------------------------
    def processRemoveBan(self,message, IsAdmin):
        text =""
        if IsAdmin:
            user = ''
            try:
                user = message.textArgs[0].replace('@','')
                self.removeBanned(user)

            except IndexError:
                print('No Arguments found for this command')
            except Exception as e:
                print('Error while handling static commands.', message)
                print(e)
            
        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"

        return text

    #-------------------------------------------------------------------------------------------------------------------------------
    def processMyBans(self,message, IsAdmin):
        text =""
        if IsAdmin:
            text = self.myBannedList()
            
        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
        return text

