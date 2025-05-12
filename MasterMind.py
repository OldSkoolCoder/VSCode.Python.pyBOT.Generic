import json
import config
from GlobalFunctions import *
import random

class MasterMind:
    def __init__(self, sio):
        self.MasterMind = {}
        self.MasterMindFilename = config.DEFAULT_JSON_DIRECTORY + 'MasterMindChart.json'
        self.MasterMindSchema= {
            "entries": 
                {}
        }

        self.GameActive = False
        self.GamePlayers = {}
        self.SecretCombination = []
        self.sio = sio

    #-------------------------------------------------------------------------------------------------------------------------------
    def readMasterMind(self):
        with open(self.MasterMindFilename, 'r') as file:
            self.MasterMind = json.load(file)
            isSchemaClean = ensureJSONSchema(self.MasterMindSchema, self.MasterMind)
            if not isSchemaClean:
                self.writeMasterMind()

    #-------------------------------------------------------------------------------------------------------------------------------
    def writeMasterMind(self):
        with open(self.MasterMindFilename, 'w') as file:
            json.dump(self.MasterMind, file,sort_keys=False,indent=2)

    #-------------------------------------------------------------------------------------------------------------------------------
    def startNewGame(self):

        self.SecretCombination.clear()
        self.GamePlayers.clear()

        for item in range(4):
            self.SecretCombination.append(random.randint(1,9))

        #self.SecretCombination = [5,2,2,4]
        self.GameActive = True
        
        self.sio.call('gamestart', 'codebreaker')

        #print(self.SecretCombination)

    #-------------------------------------------------------------------------------------------------------------------------------
    def guessAttempt(self, user, attempt):

        #print('Hello Guess')
        if self.GameActive:
            user = user.upper()

            guessFlags = ['-','-','-','-']

            try:
                code = list(map(int, attempt))
                for x in code:
                    if x < 1:
                        return f"{user}, Negative Number are stupid...., Try Again!!"
                    elif x > 9:
                        return f"{user}, Really??? above 9.... Really??...., Try Again!!"
            except ValueError:
                return f"{user}, Int Error Sorry Wrong Choice, Try Again!!"

            # Check if the right length
            if len(code) !=4:
                return f"{user}, Sorry Wrong Choice, Try Again!!"

            if user in self.GamePlayers:
                self.GamePlayers[user]['attemptNo'] += 1
            else:
                playerStats = {'attempt': '', 'attemptNo': 0, 'result': []}
                self.GamePlayers[user] = playerStats
                self.GamePlayers[user]['attemptNo'] = 1

            userCount = self.GamePlayers[user]['attemptNo']

            # Process the User Input
            dummySecretCode = [x for x in self.SecretCombination]

            # loop thru the combinations
            for x in range(4):
                if code[x] in dummySecretCode:
                    if code[x] == dummySecretCode[x]:
                        guessFlags[x] = 'B'
                        dummySecretCode[x] = 0

            # loop thru the combinations
            for x in range(4):
                if code[x] in dummySecretCode:
                    if (code[x] != dummySecretCode[x]) and guessFlags[x] == '-':
                        guessFlags[x] = 'W'
                        dummySecretCode[dummySecretCode.index(code[x])] = 0

            # for x in range(4):
            #     if dummySecretCode[x] in code:
            #         if dummySecretCode[x] == code[x]:
            #             guessFlags[x] = 'B'
            #         else:
            #             guessFlags[x] = 'W'

            #random.shuffle(guessFlags)

            self.GamePlayers[user]['attempt'] = ''.join(attempt)
            self.GamePlayers[user]['result'] = guessFlags

            if code == self.SecretCombination:
                self.GameActive = False

                if user in self.MasterMind['entries']:
                    if userCount < self.MasterMind['entries'][user]:
                        self.MasterMind['entries'][user] = userCount
                else:
                    self.MasterMind['entries'][user] = userCount
                
                self.writeMasterMind()

                self.sio.call('gameended', 'codebreaker')
                return f'{user}, Congratulations!! YOU WIN!!!! and did it in {userCount} attempt(s)'

            activePlayers = self.GamePlayers.copy()
            arrPlayers = []
            arrPlayers.clear()

            while len(activePlayers) > 0:
                arrPlayers.append(activePlayers.popitem())

            self.sio.call('gameupdate', arrPlayers)
            return f"{user} attempt #{userCount}, " + ' '.join(attempt) + " ( " +  " : ".join(guessFlags) + " )"

        else:
            return f"{user}, Sorry the game has been completed. Next Time eh?"            

    #-------------------------------------------------------------------------------------------------------------------------------
    def processStartGame(self, message, IsAdmin, CanExecute):
        text = ""
        if IsAdmin or CanExecute:
            if message.textArgs[0].lower() == 'codebreaker':
                self.startNewGame()
                text = f"@{message.user}, Has Just started a new Code Breaker Game, Enjoy"
            else:
                text = f"@{message.user}, Sorry, Dont know that game."
        else:
            text = f"@{message.user}, You dont have the permissions for this command, so SOD OFF!!! LOL"

        return text
    
    #-------------------------------------------------------------------------------------------------------------------------------
    def processGuess(self, message):

        userGuess = message.textArgs

        print (userGuess)

        if self.GameActive:
            if len(userGuess) == 1:
                userGuess = list(message.textArgs[0])
            else:
                userGuess = message.textArgs
            
            guessResult = self.guessAttempt(message.user, userGuess)

        else:
            guessResult = f"{message.user}, There is no game running currently, Sorry."

        return guessResult


