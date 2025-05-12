import json
import config
from GlobalFunctions import *

class Voting:
    def __init__(self, sio):
        self.Votes = {}
        self.VotesFilename = config.DEFAULT_JSON_DIRECTORY + 'Voting.json'
        self.VotesSchema= {
            "entries": 
                {}
        }
        self.CurrentVote = ""
        self.CurrentVoteOutOf = 10
        self.sio = sio

    #-------------------------------------------------------------------------------------------------------------------------------
    def readVotes(self):
        with open(self.VotesFilename, 'r') as file:
            self.Votes = json.load(file)
            isSchemaClean = ensureJSONSchema(self.VotesSchema, self.Votes)
            if not isSchemaClean:
                self.writeVotes()

    #-------------------------------------------------------------------------------------------------------------------------------
    def writeVotes(self):
        with open(self.VotesFilename, 'w') as file:
            json.dump(self.Votes, file,sort_keys=False,indent=2)

    #-------------------------------------------------------------------------------------------------------------------------------
    def startVote(self, vote, OutOf):
        self.CurrentVote = vote.upper() + ' Out Of ' + str(OutOf)
        self.CurrentVoteOutOf = OutOf

        UserVote = {}

        if self.CurrentVote not in self.Votes['entries']:
            self.Votes['entries'][self.CurrentVote] = UserVote 

        self.writeVotes()
        self.sio.call('gamestart', 'vote')

    #-------------------------------------------------------------------------------------------------------------------------------
    def addVote(self, username, Vote):
        username = username.upper()
        print(Vote)
        self.Votes['entries'][self.CurrentVote][username] = str(Vote)

        self.writeVotes()

        activeVotes = self.Votes['entries'][self.CurrentVote].copy()
        
        arrPlayers = []
        arrPlayers.clear()

        while len(activeVotes) > 0:
            arrPlayers.append(activeVotes.popitem())
        
        print(arrPlayers)


        self.sio.call('gameupdate', arrPlayers)

    #-------------------------------------------------------------------------------------------------------------------------------
    def endVote(self):
        self.CurrentVote = ""

        self.sio.call('gameended', 'vote')

    #-------------------------------------------------------------------------------------------------------------------------------
    def processStartVoting(self, message, IsAdmin, CanExecute):
        text = ""
        if IsAdmin or CanExecute:
            if len(message.textArgs) == 1:
                text = f"@{message.user}, Sorry, Command is !startvote Topic OutOf"
            elif self.CurrentVote == '':
                self.startVote(message.textArgs[0].lower(), int(message.textArgs[1]))
            else:
                text = f"@{message.user}, Sorry, There is a vote in progress {self.CurrentVote}."
        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"

        return text
    #-------------------------------------------------------------------------------------------------------------------------------
    def processVote(self, message):
        text = ""
        if self.CurrentVote == '':
            text = f"@{message.user}, Sorry, There is no vote in progress."
        else:
            try:
                userVote = int(message.textArgs[0])
                if userVote >= 0 and userVote <= self.CurrentVoteOutOf:
                    self.addVote(message.user, userVote)
                else:
                    text = f"@{message.user}, Im Sorry, Thats was an Invalid Vote, vote is out of {self.CurrentVoteOutOf}"
            except:
                text = f"@{message.user}, Im Sorry, This is not a Number"

        return text

    #-------------------------------------------------------------------------------------------------------------------------------
    def processCloseVoting(self, message, IsAdmin, CanExecute):
        text = ""
        if IsAdmin or CanExecute:
            if self.CurrentVote == '':
                text = f"@{message.user}, Sorry, There is no vote in progress."
            else:
                self.endVote()
        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"

        return text



