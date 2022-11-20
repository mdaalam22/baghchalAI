import time
from board import Board
import qtable
import numpy as np
from constants import TIGER, GOAT

qt = qtable.QTable()
qt_dict = qt.load('./model/best_qtable_500.pkl')

tiger_win = 0
goat_win = 0
drawn = 0

def best_move_nn(old_state, next_state_list):
    rewards = []
    for next_state in next_state_list:
        final_state = old_state.position + next_state.position + [old_state.turn]
        final_state_tp = tuple(final_state)
        reward = qt_dict.get(final_state_tp, 0)
        rewards.append(reward)
    reward_list = np.array(rewards)
    if not any(reward_list):
        print("max")
        r_max = np.argmax([state.reward for state in next_state_list])
        return next_state_list[r_max]
    return next_state_list[np.argmax(reward_list)]


def play_game(board):
    global tiger_win
    global goat_win
    global drawn
    
    board.show()
    count: int = 1

    while True:
        board.ai = board.turn
        print("Counter: ",count)
        best_moves = board.generate_possible_moves() # new
        best_move = best_move_nn(board, best_moves)
        new_pos_list = best_move.position # new
        move: str = board.get_move(board.position, new_pos_list)
        print(f"{'Tiger' if board.turn == TIGER else 'Goat'}", move)
        board = board.make_move(move)
        board.prev_moves.append(move)
        board.show()
        count += 1
        
        if board.is_draw():
            drawn += 1
            print("Game drawn")
            break

        if board.is_win():
            if -board.turn == TIGER:
                tiger_win += 1
            else: goat_win += 1

            print(f"{'Tiger' if -board.turn == TIGER else 'Goat'} win the game")
            break


if __name__ == '__main__':
    N = 1000
    for i in range(N):
        print(f"========= Game Counter {i + 1} ===========")
        board = Board()
        play_game(board)
    
    print(f"Total Tiger win: {tiger_win} ")
    print(f"Total Goat win: {goat_win} ")
    print(f"Total Drawn: {drawn} ")
