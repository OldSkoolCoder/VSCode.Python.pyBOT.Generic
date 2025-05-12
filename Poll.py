import json
import config
from GlobalFunctions import *

class Poll:
    def __init__(self, sio):
        self.Polls = {}
        self.PollsFilename = config.DEFAULT_JSON_DIRECTORY + 'Polls.json'
        self.PollsSchema= {
            "entries": 
                {}
        }
        self.CurrentPoll = ""
        self.PollYes = ""
        self.PollNo = ""
        self.sio = sio
        self.WhosVoted = []

    #-------------------------------------------------------------------------------------------------------------------------------
    def readPolls(self):
        with open(self.PollsFilename, 'r') as file:
            self.Polls = json.load(file)
            isSchemaClean = ensureJSONSchema(self.PollsSchema, self.Polls)
            if not isSchemaClean:
                self.writePolls()

    #-------------------------------------------------------------------------------------------------------------------------------
    def writePolls(self):
        with open(self.PollsFilename, 'w') as file:
            json.dump(self.Polls, file,sort_keys=False,indent=2)

    #-------------------------------------------------------------------------------------------------------------------------------
    def startPoll(self, Question, Yes, No):
        self.CurrentPoll = Question.upper()

        self.PollYes = Yes.upper()
        self.PollNo = No.upper()
        UserPoll = {}
        self.WhosVoted.clear()

        if self.CurrentPoll not in self.Polls['entries']:
            self.Polls['entries'][self.CurrentPoll] = UserPoll
            self.Polls['entries'][self.CurrentPoll][self.PollYes] = 0
            self.Polls['entries'][self.CurrentPoll][self.PollNo] = 0

        self.writePolls()
        self.sio.call('pollstart', [Question,Yes,No])

    #-------------------------------------------------------------------------------------------------------------------------------
    def addPoll(self, username, Poll, Admin):
        username = username.upper()
        Poll = Poll.upper()
        print(f"User {username} polled {Poll}")

        if username not in self.WhosVoted or Admin == True:
            if Poll in self.Polls['entries'][self.CurrentPoll]:
                self.Polls['entries'][self.CurrentPoll][Poll] += 1

                self.WhosVoted.append(username)
                self.writePolls()

                Yes = self.Polls['entries'][self.CurrentPoll][self.PollYes]
                No = self.Polls['entries'][self.CurrentPoll][self.PollNo]

                YesWidth = int((Yes / (Yes+No))*100)
                NoWidth = 100 - YesWidth
                arrData = [YesWidth,NoWidth]

                self.sio.call('pollupdate', arrData)
                return ""
            else:
                return f"@{username} oh C'mon, cant you read, the right answer is either '{self.PollYes}' or '{self.PollNo}' you idiot!!"
        else:
            return f"@{username} you idiot!!, trying to rig the poll"

    #-------------------------------------------------------------------------------------------------------------------------------
    def endPoll(self):
        self.CurrentPoll = ""
        self.PollNo = ""
        self.PollYes = ""

        self.sio.call('pollended', '')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processStartPoll(self, message, IsAdmin):
        if IsAdmin:
            if len(message.textArgs) == 1:
                text = f"@{message.user}, Sorry, Command is !startpoll Yes No Topic"
            elif self.CurrentPoll == '':
                Yes = message.textArgs.pop(0).upper()
                No = message.textArgs.pop(0).upper()

                self.startPoll(' '.join(message.textArgs), Yes, No)
                text = ""
            else:
                text = f"@{message.user}, Sorry, There is a poll in progress {self.Poll.CurrentPoll}."
        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
        return text            

    #-------------------------------------------------------------------------------------------------------------------------------
    def processPoll(self, message, IsAdmin):
        if self.CurrentPoll == '':
            text = f"@{message.user}, Sorry, There is no poll in progress."
        else:
            # try:
                userPoll = message.textArgs[0]
                text = self.addPoll(message.user, userPoll, IsAdmin)
            # except:
            #     text = f"@{message.user}, Im Sorry, This is not a Number"
            #     self.sendPrivmsg(message.channel, text)            
        return text

    #-------------------------------------------------------------------------------------------------------------------------------
    def processClosePoll(self, message, IsAdmin):
        if IsAdmin:
            if self.CurrentPoll == '':
                text = f"@{message.user}, Sorry, There is no poll in progress."
            else:
                self.Poll.endPoll()
                text = ""
        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"
        return text
