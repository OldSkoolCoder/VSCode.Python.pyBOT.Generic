import json
import config
from GlobalFunctions import *

class ChatPoints:
    def __init__(self):
        self.Points = {}
        self.PointsFilename = config.DEFAULT_JSON_DIRECTORY + 'OSKPoints.json'
        self.PointsSchema= {
            "entries": 
                {}
        }

    #-------------------------------------------------------------------------------------------------------------------------------
    def readPoints(self):
        with open(self.PointsFilename, 'r') as file:
            self.Points = json.load(file)
            isSchemaClean = ensureJSONSchema(self.PointsSchema, self.Points)
            if not isSchemaClean:
                self.writePoints()

    #-------------------------------------------------------------------------------------------------------------------------------
    def writePoints(self):
        with open(self.PointsFilename, 'w') as file:
            json.dump(self.Points, file,sort_keys=False,indent=2)

    #-------------------------------------------------------------------------------------------------------------------------------
    def addPoints(self, username, points):
        username = username.upper()
        if username in self.Points['entries']:
            self.Points['entries'][username] += points
        else:
            self.Points['entries'][username] = points

        self.writePoints()

        return self.Points['entries'][username]

    #-------------------------------------------------------------------------------------------------------------------------------
    def subPoints(self, username, points):
        username = username.upper()
        if username in self.Points['entries']:
            self.Points['entries'][username] -= points
        else:
            self.Points['entries'][username] = points

        self.writePoints()

        return self.Points['entries'][username]

    #-------------------------------------------------------------------------------------------------------------------------------
    def myPoints(self, username):
        username = username.upper()
        if username not in self.Points['entries']:
            self.Points['entries'][username] = 0

        self.writePoints()

        return self.Points['entries'][username]        

    #-------------------------------------------------------------------------------------------------------------------------------
    def top10Points(self):
        return sorted(self.Points['entries'].items(), key=lambda item: item[1], reverse = True)

    #-------------------------------------------------------------------------------------------------------------------------------
    def processAddPoints(self, message, CanExecute):
        text = ""
        if CanExecute:
            try:
                points = int(message.textArgs[1])
                if points <=0:
                    text = f'{message.user}, really, negative or zero points.... whats the point in that :p'
                else:
                    accumulatedPoints = self.addPoints(message.textArgs[0].replace('@',''), points)
                    text = f'{message.textArgs[0]}, has {accumulatedPoints} {config.POINTSNAME} now'
            except IndexError:
                text = f"@{message.user} Your command is missing some arguments!"
            except Exception as e:
                print('Error while handling static commands.', message)
                print(e)
        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"

        return text

    #-------------------------------------------------------------------------------------------------------------------------------
    def processSubPoints(self, message, CanExecute):
        text = ""
        if CanExecute:
            try:
                points = int(message.textArgs[1])
                if points <=0:
                    text = f'{message.user}, really, negative or zero points.... whats the point in that :p'
                else:
                    accumulatedPoints = self.subPoints(message.textArgs[0].replace('@',''), points)
                    text = f'{message.textArgs[0]}, has {accumulatedPoints} {config.POINTSNAME} now'
            except IndexError:
                text = f"@{message.user} Your command is missing some arguments!"
            except Exception as e:
                print('Error while handling static commands.', message) 
                print(e)
        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
        return text

    #-------------------------------------------------------------------------------------------------------------------------------
    def processMyPoints(self, message):
        myPoints = self.myPoints(message.user.replace('@',''))
        if myPoints == 0:
            text = f'{message.user}, has {myPoints} {config.POINTSNAME}, what a LOSER!'
        else:
            text = f'{message.user}, has {myPoints} {config.POINTSNAME} now'
        return text
    
    #-------------------------------------------------------------------------------------------------------------------------------
    def processTop10Points(self, message, BOT):
        sortedPoints = self.top10Points()

        chartPosition = 0
        for item in sortedPoints:
            chartPosition +=1
            if chartPosition > 10:
                break
            BOT.sendPrivmsg(message.channel, f'{chartPosition}. {item[0]}, has {item[1]} {config.POINTSNAME}', '')

