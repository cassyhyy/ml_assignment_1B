#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying 
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
import util 
import sys
import random
import time
from optparse import OptionParser

class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """
    def __init__(self):
        """
          Represent 3 boards with lists of boolean value 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]: 
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)

class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}
        self.Q_dict = self.getQVariable()[0]
        self.Q_monoid = self.getQVariable()[1]
        self.Q_monoidDict = self.getQVariable()[2]
        self.Q_pPostion = self.getQVariable()[3]
        self.Q_nPosition = self.getQVariable()[4]
        
    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])

    # 初始化一些Q相关变量
    def getQVariable(self):
        QDict = self.getQDict()
        monoid = set(['1', 'a', 'b', 'ab', 'bb', 'abb', 'c', 'ac', 'bc', 'abc', 'cc', 'acc', 'bcc', 'abcc', 'd', 'ad', 'bd', 'abd'])
        # Q =〈a, b, c, d | a2 = 1, b3 = b, b2c = c, c3 = ac2, b2d = d, cd = ad, d2 = c2〉
        monoidDict = {'aa': '1', 'bbb': 'b', 'bbc': 'c', 'ccc': 'acc', 'bbd': 'd', 'cd': 'ad', 'dd': 'cc'}
        pPosition = set(['a', 'bb', 'bc', 'cc'])
        nPosition = monoid - pPosition
        return (QDict, monoid, monoidDict, pPosition, nPosition)

    # 依据102种情况的board情况获得相应的Q值
    def getQDict(self):
        # 依据图中102种情况创建QList（去除dead情况）
        QList = \
            [   # 第1行
                [[False, False, False, False, False, False, False, False, False], 'c'],
                [[True, False, False, False, False, False, False, False, False], '1'],
                [[False, True, False, False, False, False, False, False, False], '1'],
                [[False, False, False, False, True, False, False, False, False], 'cc'],
                [[True, True, False, False, False, False, False, False, False], 'ad'],
                [[True, False, True, False, False, False, False, False, False], 'b'],
                [[True, False, False, False, True, False, False, False, False], 'b'],
                [[True, False, False, False, False, True, False, False, False], 'b'],
                [[True, False, False, False, False, False, False, False, True], 'a'],
                # 第2行
                [[False, True, False, True, False, False, False, False, False], 'a'],
                [[False, True, False, False, True, False, False, False, False], 'b'],
                [[False, True, False, False, False, False, False, True, False], 'a'],
                [[True, True, False, True, False, False, False, False, False], 'b'],
                [[True, True, False, False, True, False, False, False, False], 'ab'],
                [[True, True, False, False, False, True, False, False, False], 'd'],
                [[True, True, False, False, False, False, True, False, False], 'a'],
                [[True, True, False, False, False, False, False, True, False], 'd'],
                # 第3行
                [[True, True, False, False, False, False, False, False, True], 'd'],
                [[True, False, True, False, True, False, False, False, False], 'a'],
                [[True, False, True, False, False, False, True, False, False], 'ab'],
                [[True, False, True, False, False, False, False, True, False], 'a'],
                [[True, False, False, False, True, True, False, False, False], 'a'],
                [[True, False, False, False, False, True, False, True, False], '1'],
                [[False, True, False, True, True, False, False, False, False], 'ab'],
                [[False, True, False, True, False, True, False, False, False], 'b'],
                # 第4行
                [[True, True, False, True, True, False, False, False, False], 'a'],
                [[True, True, False, True, False, True, False, False, False], 'a'],
                [[True, True, False, True, False, False, False, False, True], 'a'],
                [[True, True, False, False, True, True, False, False, False], 'b'],
                # 第5行
                [[True, True, False, False, True, False, True, False, False], 'b'],
                [[True, True, False, False, False, True, True, False, False], 'b'],
                [[True, True, False, False, False, True, False, True, False], 'ab'],
                [[True, True, False, False, False, True, False, False, True], 'ab'],
                [[True, True, False, False, False, False, True, True, False], 'b'],
                [[True, True, False, False, False, False, True, False, True], 'b'],
                [[True, True, False, False, False, False, False, True, True], 'a'],
                # 第6行
                [[True, False, True, False, True, False, False, True, False], 'b'],
                [[True, False, True, False, False, False, True, False, True], 'a'],
                [[True, False, False, False, True, True, False, True, False], 'b'],
                [[False, True, False, True, False, True, False, True, False], 'a'],
                # 第7行
                [[True, True, False, True, False, True, False, True, False], 'b'],
                # 第8行
                [[True, True, False, True, False, True, False, False, True], 'b'],
                [[True, True, False, False, True, True, True, False, False], 'a'],
                [[True, True, False, False, False, True, True, True, False], 'a'],
                [[True, True, False, False, False, True, True, False, True], 'a'],
                # 第9行全为dead状态
                # 第10行
                [[True, True, False, True, False, True, False, True, True], 'a']
            ]
        dict = {}
        for board, value in QList:
            # 将board上下、左右旋转，并加入dict
            for i in range(2):
                board = self.rotateBoardXY(board)
                for j in range(4):
                    board = self.rotateBoard(board)
                    key = self.boardToString(board)
                    if key not in dict:
                        dict.update({key: value})
        return dict

    # 将board转换为string类型，便于做Q_dict的key
    def boardToString(self, board):
        result = str()
        for b in board:
            if b:
                result += "T"
            else:
                result += "F"
        return result

    # 逆时针旋转board 90°
    def rotateBoard(self, board):
        return [board[6], board[3], board[0], board[7], board[4], board[1], board[8], board[5], board[2]]

    # 上下旋转board
    def rotateBoardXY(self, board):
        return [board[6],board[7],board[8],board[3],board[4],board[5],board[0],board[1],board[2]]

    # 获取当前3个board的QValue的乘积
    def getQValues(self, boards):
        value = ''
        for board in boards:
            if not self.deadTest(board):
                key = self.boardToString(board)
                value += self.Q_dict.get(key)  # 字符串拼接
        return self.getMonoidQ(value)

    # 简化value到monoid_Q
    def getMonoidQ(self, value):
        result = self.sortString(value)
        while result not in self.Q_monoid:
            for key in self.Q_monoidDict:
                result = self.haveSequence(result, key, self.Q_monoidDict.get(key))
        return result

    # 字符串升序排列
    def sortString(self, str):
        # 字符串当中只有1时返回'1'
        onlyOne = True
        for s in str:
            if s != '1':
                onlyOne = False
                break
        if onlyOne or str == '':
            return '1'
        # 字符串升序排序
        l = list(str)
        l.sort()
        return "".join(l).lstrip('1')

    # 判断字符串中是否有子序列key，并返回对应覆盖了value后的字符串
    def haveSequence(self, str, key, value):
        if key == 'bbd':
            # 分2段考虑
            index = str.find('bb')
            index2 = str.find('d')
            if index >= 0 and index2 > 0:
                return self.sortString(str[0:index]+str[index+2:index2]+str[index2+1:]+value)
            else:
                return str
        else:
            index = str.find(key)
            if index >= 0:
                return self.sortString(str[0:index]+str[index+len(key):]+value)
            else:
                return str

class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}
        self.depth = 1.5

    def getAction(self, gameState, gameRules):
        # legalActions = gameState.getLegalActions(gameRules)
        # actions = []
        # for action in legalActions:
        #     newBoards = gameState.generateSuccessor(action).boards
        #     value = gameRules.getQValues(newBoards)
        #     # 如果QValue在P-Position中，该行动赢的几率大
        #     if value in gameRules.Q_pPostion:
        #         # return action
        #         actions.append(action)
        # if len(actions) > 0:
        #     return random.choice(actions)
        # else:
        #     return random.choice(legalActions)
        return self.minimax(gameState, gameRules, 0)[0]
        util.raiseNotDefined()

    # 估算函数，如果当前状态为Q_pPosition，返回10，否则返回-10
    def evaluationFunction(self, gameState, gameRules):
        if gameRules.getQValues(gameState.boards) in gameRules.Q_pPostion:
            return 10
        else:
            return -10

    # minimax的递归，返回(action, bestScore)
    def minimax(self, gameState, gameRules, depth):
        # 游戏结束
        if gameRules.isGameOver(gameState.boards):
            # 如果当前节点为玩家节点(max)，即AI让棋盘dead了，玩家胜利，则返回一个高的值
            if depth % 2 == 0:
                return (None, 100)
            else:
                return (None, -100)
        # 到达最深层
        if depth == self.depth * 2:
            return (None, self.evaluationFunction(gameState, gameRules))
        legalMoves = gameState.getLegalActions(gameRules)
        successor = []
        for action in legalMoves:
            successor.append(gameState.generateSuccessor(action))
        value = []
        for newState in successor:
            value.append(self.minimax(newState, gameRules, depth + 1)[1])
        # print(depth, value)
        if depth % 2 == 0:
            bestValue = max(value)
        else:
            bestValue = min(value)
        bestIndices = [index for index in range(len(value)) if value[index] == bestValue]
        chosenIndex = random.choice(bestIndices)
        return (legalMoves[chosenIndex], bestValue)

class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """
    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)


class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """
    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action 

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 30 

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    # random.seed(1)
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
