from cmath import exp
import numpy as np
from qtable import QTable
from mcts import MCTS

class Agent:
    """ The Agent plays the game by playing a move corresponding to the optimal Q-value """

    def __init__(
        self, qtable=None, epsilon=0.2, learning_rate=0.3, discount_factor=0.9
    ):
        """ A new Agent can be given some optional parameters to tune how fast it learns
        
        Args:
            qtable: QTable=None: the initial Q-table to start with. 
            epsilon: float=0.2: the chance the Agent will explore a random move
                               (in stead of choosing the optimal choice according to the Q table)
            learning_rate: float=0.3: the rate at which the Agent learns from its games
            discount_factor: float=0.9: the rate at which the final reward gets discounted
                                        for when rating previous moves.
        """
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
            # Choose action (random with chance of epsilon; best action otherwise.)
            #----- new line start--------
            best_move = mcts.search(state)
            new_pos_list= best_move.board.position
            action = state.get_move(state.position, new_pos_list)

            # ------ new line end
            # action = self.random_action()
        else:
            # get qvalues for current state of the game
            action = self.best_action(state)

        return action

    def learn(self, state, action, next_state, reward):
        """ learn from the current state and action taken. """
        state2d, turn = state.position, state.turn
        next_state2d= next_state.position
        final_state = state2d + next_state2d + [turn]
        final_state = tuple(final_state)
        # if next_turn == 0:  # game finished
        #     expected_qvalue_for_action = reward
        # else:
        #     next_qvalues = self.qtable(final_state)
        #     next_qvalues = 0 if next_qvalues is None else next_qvalues
        #     # minmax = {1: max, -1: min}[next_turn]
        #     expected_qvalue_for_action = reward + (
        #         self.discount_factor * next_qvalues
        #     )

        # update qvalues:

        # ---- update qvalues -----------  
        _value = self.qtable._qtable.get(final_state, 0)
        _target = reward + self.discount_factor * _value
        _delta = abs(_target - state.reward)
        self.qtable._qtable[final_state] = _value +  self.learning_rate * _delta
        #-------------------------------
        # # qvalues = self.qtable(state2d)
        # # qvalues[action] += self.learning_rate * (
        # #     expected_qvalue_for_action - qvalues[action]
        # # )
        # # final_state = state2d + next_state2d + [turn]
        # qvalues = self.qtable(final_state)
        # if qvalues is None:
        #     self.qtable._qtable[final_state] = reward
        # else: 
        #     self.qtable._qtable[final_state] = expected_qvalue_for_action if self.qtable[final_state] < expected_qvalue_for_action else self.qtable[final_state]