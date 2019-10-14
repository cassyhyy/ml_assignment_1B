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

          gameState.isLose():http://www.zimuxia.cn/
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, 0, 0)[0]
        util.raiseNotDefined()

    # minimax的递归，返回(action, bestScore)
    def minimax(self, gameState, agent, depth):
        if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        legalMoves = gameState.getLegalActions(agent)
        successor = []
        for action in legalMoves:
            successor.append(gameState.generateSuccessor(agent, action))
        value = []
        if agent == 0:
            for newState in successor:
                value.append(self.minimax(newState, 1, depth + 1)[1])
            bestValue = max(value)
        else:
            for newState in successor:
                # 当鬼的数目大于2时，需要多层min layer
                if agent + 1 < gameState.getNumAgents():
                    value.append(self.minimax(newState, agent + 1, depth + 1)[1])
                else:
                    # 当鬼的min layer都遍历完时，重新回到agent=0
                    value.append(self.minimax(newState, 0, depth + 1)[1])
            bestValue = min(value)
        bestIndices = [index for index in range(len(value)) if value[index] == bestValue]
        chosenIndex = random.choice(bestIndices)
        return (legalMoves[chosenIndex], bestValue)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, 0, 0, -9999, 9999)[0]
        util.raiseNotDefined()

    def minimax(self, gameState, agent, depth, alpha, beta):
        if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        legalMoves = gameState.getLegalActions(agent)
        maxValue = -9999
        minValue = 9999
        if agent == 0:
            # find max: 判断v>beta？
            for action in legalMoves:
                newState = gameState.generateSuccessor(agent, action)
                value = self.minimax(newState, 1, depth + 1, alpha, beta)[1]
                if value > maxValue:
                    maxValue = value
                    chooseAction = action
                    if value > beta:
                        return (chooseAction, maxValue)
                # max结点：确定alpha
                alpha = max(alpha, maxValue)
        else:
            # find min: 判断v<alpha？
            if agent + 1 < gameState.getNumAgents():
                nextAgent = agent + 1
            else:
                nextAgent = 0
            for action in legalMoves:
                newState = gameState.generateSuccessor(agent, action)
                value = self.minimax(newState, nextAgent, depth + 1, alpha, beta)[1]
                if value < minValue:
                    minValue = value
                    chooseAction = action
                    if value < alpha:
                        return (chooseAction, minValue)
                # min结点：确定beta
                beta = min(beta, minValue)
        # 依据agentIndex记录result，当agent为pacman时取max，为ghost时取min
        if agent == 0:
            result = maxValue
        else:
            result = minValue
        return (chooseAction, result)

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
        return self.expectimax(gameState, 0, 0)[0]
        util.raiseNotDefined()

    # expectimax的递归，返回(action, bestScore)
    def expectimax(self, gameState, agent, depth):
        # 当遍历深度足够或者游戏结束时，返回(None,当前分数)
        if depth == gameState.getNumAgents() * self.depth or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        # 记录变量
        legalMoves = gameState.getLegalActions(agent)
        probability = 1.0 / len(legalMoves)
        scores = []
        averageScore = 0
        for action in legalMoves:
            newState = gameState.generateSuccessor(agent, action)
            if agent==0:
                scores.append(self.expectimax(newState, 1, depth + 1)[1])
            else:
                if agent+1 < gameState.getNumAgents():
                    nextAgent = agent + 1
                else:
                    nextAgent = 0
                averageScore += probability * self.expectimax(newState, nextAgent, depth + 1)[1]
        # 当前agent为ghost时，返回averageScore；为pacman时返回最大分数
        if agent != 0:
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

