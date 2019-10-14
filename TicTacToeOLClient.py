#!/bin/python

import util
from solveTicTacToe import GameState, GameRules, TicTacToeAgent

import requests
from optparse import OptionParser
import json
import time
import re

settings = {
    "host": "https://study.ny-do.com",
    "port": 443,
    "url": "/tictactoe",

    "username": "",
}

class RemoteAgent():
    def newGame(self, username, serverOrder):
        self.sess = requests.session()
        res = self.sess.post("%s:%d%s" % (settings["host"], settings["port"], settings["url"]),
        json={
            "status": "Start",
            "username": username,
            "serverOrder": "First" if serverOrder == 1 else "Second",
        })
        if res.status_code == 200:
            pass
        else:
            raise Exception("Fail to connect to server.")

        res, msg = self.queryResponse()
        if res.status_code == 200 \
            and msg["message"] == "Query Response." \
            and msg["info"]["status"] == "New Game":
            pass
        else:
            raise Exception("Fail to connect to server.")
    
    def finishGame(self):
        res = self.sess.post("%s:%d%s" % (settings["host"], settings["port"], settings["url"]),
        json={
            "status": "Terminate",
        })
        if res.status_code == 200:
            pass
        else:
            raise Exception("Connection reset.")

    def queryResponse(self):
        while True:
            res = self.sess.post("%s:%d%s" % (settings["host"], settings["port"], settings["url"]),
            json={
                "status": "Query",
            })
            # print(res, res.text)
            if res.text != None:
                msg = json.loads(res.text)
                if res.status_code == 200 and msg["message"] == "Try again.":
                    pass
                else:
                    return res, msg
            time.sleep(1)

    def inform(self, rivalAction):
        res = self.sess.post("%s:%d%s" % (settings["host"], settings["port"], settings["url"]),
        json={
            "status": "Action",
            "action": rivalAction,
        })
        if res.status_code == 200:
            pass
        else:
            raise Exception("Connection reset.")

    def getAction(self, gameState, gameRules):
        res, msg = self.queryResponse()
        if res.status_code == 200 and msg["message"] == "Query Response.":
            if msg["info"]["status"] == "Action":
                return msg["info"]["msg"]
        raise Exception("Connection reset.")

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, username, numOfGames, localOrder, muteOutput, maxTimeOut):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        assert(int(localOrder) in [1, 2])

        self.username = str(username) if username != "" else str(settings["username"])
        if not re.match("[a-zA-Z0-9]+", self.username) or self.username == "demo":
            raise Exception("Invalid username (only letters and digits are allowed). Use -u to specify a username or edit in settings variable.")

        self.numOfGames = int(numOfGames)
        self.localOrder = int(localOrder)
        self.muteOutput = bool(muteOutput)
        self.maxTimeOut  = int(maxTimeOut)
        self.gameRules   = GameRules()

        if localOrder == 1:
            self.firstAgent = TicTacToeAgent()
            self.secondAgent = RemoteAgent()
            print("Player 1 is local agent; Player 2 is remote agent.")
        elif localOrder == 2:
            self.firstAgent = RemoteAgent()
            self.secondAgent = TicTacToeAgent()
            print("Player 1 is remote agent; Player 2 is local agent.")

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        remoteAgent = self.secondAgent if self.localOrder == 1 else self.firstAgent
        numOfWins = 0
        for i in range(self.numOfGames):
            try:
                remoteAgent.newGame(self.username, 3 - self.localOrder)
                gameState = GameState()
                agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
                while True:
                    playerIndex = agentIndex + 1
                    timed_func = util.TimeoutFunction(self.firstAgent.getAction if agentIndex == 0 else self.secondAgent.getAction, self.maxTimeOut)
                    try:
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException as err:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (playerIndex, self.maxTimeOut))
                        raise err
                    if not self.muteOutput:
                        print("Player %d: %s" % (playerIndex, action))
                    if playerIndex == self.localOrder:
                        remoteAgent.inform(action)
                    gameState = gameState.generateSuccessor(action)
                    if self.gameRules.isGameOver(gameState.boards):
                        break
                    if not self.muteOutput:
                        gameState.printBoards(self.gameRules)

                    agentIndex  = (agentIndex + 1) % 2
                playerIndex = (agentIndex + 1) % 2 + 1
                print("****Player %d wins game %d!!****" % (playerIndex, i+1))
                if playerIndex == self.localOrder:
                    numOfWins += 1
                remoteAgent.finishGame()
            except Exception as err:
                print("ERROR:", err)
                time.sleep(0.5)
        print("\n****Local player wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))

if __name__ == "__main__":
    """
      main function
      -u: Username, must not be empty nor be "demo"
      -n: Indicates the number of games
      -o: Your agent's order, 1 means the first player, 2 means the second player
      -m: If specified, the program will mute the output
      -t: Max time out, 60 seconds at most
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    #random.seed(1)
    parser = OptionParser()
    parser.add_option("-u", dest="username", default="", type="str", help="Username, must not be empty nor be \"demo\"")
    parser.add_option("-n", dest="numOfGames", default=1, type="int", help="Indicates the number of games")
    parser.add_option("-o", dest="localOrder", default=1, type="int", help="Your agent's order, 1 means the first player, 2 means the second player")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False, help="If specified, the program will mute the output")
    parser.add_option("-t", dest="maxTimeOut", default=30, type="int", help="Max time out, 60 seconds at most")
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.username, options.numOfGames, options.localOrder, options.muteOutput, options.maxTimeOut)
    ticTacToeGame.run()

