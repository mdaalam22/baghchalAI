from cmath import exp
import numpy as np
from qtable import QTable
from mcts import MCTS

class Agent:
    def __init__(
        self, qtable=None, epsilon=0.2, learning_rate=0.3, discount_factor=0.9
    ):
    
        self.qtable = QTable() if qtable is None else qtable

        # the speed at which the Qvalues get updated
        self.learning_rate = learning_rate

        # the discount factor of future rewards
        self.discount_factor = discount_factor

        # the chance of executing a random action
        self.epsilon = epsilon

    def random_action(self):
        """ get a random action """
        return int(np.random.randint(0, 9, 1))

    def best_action(self, state):
        """ get the best values according to the current Q table """
        state2d, turn = state
        argminmax = {1: np.argmax, 2: np.argmin}[turn]
        qvalues = self.qtable(state2d)
        return argminmax(qvalues)

    def get_action(self, state):
        """ perform an action according to the state on the game board """
        mcts = MCTS()
        if np.random.rand() < self.epsilon:
            best_move = mcts.search(state)
            new_pos_list= best_move.board.position
            action = state.get_move(state.position, new_pos_list)
        else:
            action = self.best_action(state)

        return action

    def learn(self, state, action, next_state, reward):
        """ learn from the current state and action taken. """
        state2d, turn = state.position, state.turn
        next_state2d= next_state.position
        final_state = state2d + next_state2d + [turn]
        final_state = tuple(final_state)

        # ---- update qvalues -----------  
        _value = self.qtable._qtable.get(final_state, 0)
        _target = reward + self.discount_factor * _value
        _delta = abs(_target - state.reward)
        self.qtable._qtable[final_state] = _value +  self.learning_rate * _delta
       