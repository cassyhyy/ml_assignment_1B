from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition() #(x,y)
        newFood = successorGameState.getFood() #foodGrid
        newGhostStates = successorGameState.getGhostStates() #game.AgentState
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        maxNum = newFood.width + newFood.height
        minGhostDistance = maxNum  # 离鬼的最小距离
        eatGhostChance = 0 # 吃掉鬼的机会
        # 获取pacman距最近鬼的距离
        for state in newGhostStates:
            ghostDistance = manhattanDistance(newPos, state.getPosition())
            # if ghostDistance < minGhostDistance and state.scaredTimer:
            #     minGhostDistance = ghostDistance
            if state.scaredTimer - ghostDistance > eatGhostChance:
                eatGhostChance = state.scaredTimer - ghostDistance
            # 当不能吃掉鬼时，才计算与鬼的距离
            elif ghostDistance < minGhostDistance:
                minGhostDistance = ghostDistance
        # 获取pacman距最近食物的距离
        foodPosition = newFood.asList()
        minFoodDistance = 0
        if len(foodPosition) > 0:
            minFoodDistance = min([manhattanDistance(newPos,p) for p in foodPosition])
        # pacman离鬼、食物最近距离要+1才做倒数处理，因为可能被除数=0
        result = successorGameState.getScore() - 1.0/(minGhostDistance+1) + 1.0/(minFoodDistance+1) + eatGhostChance
        return result


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, 0)[0]
        util.raiseNotDefined()

    # minimax的递归，返回(action, bestScore)
    def minimax(self, gameState, depth):
        agentNum = gameState.getNumAgents()
        # 当遍历深度足够或者游戏结束时，返回(None,当前分数)
        if depth == agentNum * self.depth or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        # 记录变量
        agentIndex = depth % agentNum
        legalMoves = gameState.getLegalActions(agentIndex)
        scores = []
        for action in legalMoves:
            newState = gameState.generateSuccessor(agentIndex, action)
            scores.append(self.minimax(newState, depth+1)[1])
        # 依据agentIndex记录bestScores，当agent为pacman时取scores的最大值，为ghost时取最小值
        if agentIndex == 0:
            bestScore = max(scores)
        else:
            bestScore = min(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
        return (legalMoves[chosenIndex], bestScore)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, 0, -9999, 9999)[0]
        util.raiseNotDefined()

    # minimax的递归，返回(action, bestScore, aplha, beta)
    def minimax(self, gameState, depth, alpha, beta):
        agentNum = gameState.getNumAgents()
        # 当遍历深度足够或者游戏结束时，返回(None,当前分数)
        if depth == agentNum * self.depth or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        # 记录变量
        agentIndex = depth % agentNum
        legalMoves = gameState.getLegalActions(agentIndex)
        minScore = 9999
        maxScore = -9999
        for action in legalMoves:
            newState = gameState.generateSuccessor(agentIndex, action)
            value = self.minimax(newState, depth + 1, alpha, beta)[1]
            if agentIndex == 0:
                # find max: 判断v>beta？
                if value >= maxScore:
                    maxScore = value
                    chooseAction = action
                    if value > beta:
                        return (chooseAction, maxScore)
                # max结点：确定alpha
                alpha = max(alpha, maxScore)
            else:
                # find min: 判断v<alpha?
                if value <= minScore:
                    minScore = value
                    chooseAction = action
                    if value < alpha:
                        return (chooseAction, minScore)
                # min结点：确定beta
                beta = min(beta, minScore)
        # 依据agentIndex记录bestScore，当agent为pacman时取max，为ghost时取min
        if agentIndex == 0:
            bestScore = maxScore
        else:
            bestScore = minScore
        return (chooseAction, bestScore)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax(gameState, 0)[0]
        util.raiseNotDefined()

    # expectimax的递归，返回(action, bestScore)
    def expectimax(self, gameState, depth):
        agentNum = gameState.getNumAgents()
        # 当遍历深度足够或者游戏结束时，返回(None,当前分数)
        if depth == agentNum * self.depth or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        # 记录变量
        agentIndex = depth % agentNum
        legalMoves = gameState.getLegalActions(agentIndex)
        probability = 1.0 / len(legalMoves)
        scores = []
        averageScore = 0
        for action in legalMoves:
            newState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == 0:
                scores.append(self.expectimax(newState, depth + 1)[1])
            else:
                averageScore += probability * self.expectimax(newState, depth + 1)[1]
        # 当前agent为ghost时，返回averageScore；为pacman时返回最大分数
        if agentIndex != 0:
            return (None, averageScore)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best
        return (legalMoves[chosenIndex], bestScore)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # 同第一题思路差不多
    pacmanPos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    food = currentGameState.getFood()
    maxNum = food.width + food.height
    minGhostDistance = maxNum  # 离鬼的最小距离
    eatGhostChance = 0  # 吃掉鬼的机会
    # 获取pacman距最近鬼的距离
    for state in ghostStates:
        ghostDistance = manhattanDistance(pacmanPos, state.getPosition())
        # if ghostDistance < minGhostDistance and state.scaredTimer:
        #     minGhostDistance = ghostDistance
        if state.scaredTimer - ghostDistance > eatGhostChance:
            eatGhostChance = state.scaredTimer - ghostDistance
        # 当不能吃掉鬼时，才计算与鬼的距离
        elif ghostDistance < minGhostDistance:
            minGhostDistance = ghostDistance
    # 获取pacman距最近食物的距离
    foodPosition = food.asList()
    minFoodDistance = 0
    if len(foodPosition) > 0:
        minFoodDistance = min([manhattanDistance(pacmanPos, p) for p in foodPosition])
    # pacman离鬼、食物最近距离要+1才做倒数处理，因为可能被除数=0
    result = currentGameState.getScore() - 1.0 / (minGhostDistance + 1) + 1.0 / (minFoodDistance + 1) + eatGhostChance
    return result
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

