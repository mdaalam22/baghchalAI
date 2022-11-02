from mcts import MCTS, TreeNode
import time
from typing import List
from constants import TIGER
from board import Board
from qtable import QTable
from agent import Agent
from copy import deepcopy
from tqdm import tqdm
import pickle

tiger_win = 0
goat_win = 0
game_draw = 0

final_dict = {}


def game_loop(board):
    global final_dict
    global tiger_win
    global goat_win
    global game_draw

    # board.show()
    count: int = 1
    # mcts: MCTS = MCTS()
    
    qtable = QTable()  # share Q for faster training
    player = Agent(qtable=qtable, learning_rate=0.1, epsilon=2)
    
    # board play
    while True:
        print("Counter: ",count)
        board.ai = board.turn
        # best_move: TreeNode = mcts.search(board)
        # new_pos_list: List[int] = best_move.board.position
        # move: str = board.get_move(board.position, new_pos_list)

        # new line start
        prev_board = deepcopy(board)
        action  = player.get_action(board)
        board = board.make_move(action)
        board.prev_moves.append(action)
        print(board.prev_moves)
        # if board.is_draw() or board.is_win(): board.turn = 0
        player.learn(prev_board, action, board, board.reward)
        # new line end 

        print(f"{'Tiger' if board.turn == TIGER else 'Goat'}", action)
        # board = board.make_move(move)
        # board.prev_moves.append(action)
        board.show()
        count += 1
        # print(board.prev_moves)
        
        if board.is_draw():
            game_draw += 1
            print("Game drawn")
            break

        if board.is_win():
            if -board.turn == TIGER: tiger_win += 1
            else: goat_win += 1
            print(f"{'Tiger' if -board.turn == TIGER else 'Goat'} win the game")
            break
    
    # print(qtable._qtable)
    final_dict.update(qtable._qtable)


if __name__ == '__main__':
    N = 1000  # Number of training episodes
    start = time.time()
    # for _ in tqdm.trange(N):
    #     game.play()
    for i in range(N):
        print(f"=====Game: {i+1}========")
        board = Board()
        game_loop(board)
    
    end = time.time()
    print("Tiger win: ",tiger_win)
    print("goat_win: ",goat_win)
    print("Draw: ",game_draw)
    # qtable.save('best_qtable2.pkl')
    print("total state recorded: ",len(final_dict))
    with open('best_qtable_500.pkl', 'wb') as f:
        pickle.dump(final_dict, f)
   
    print(f"Time Taken: {end-start:.2f}s")

    

