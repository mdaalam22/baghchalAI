from mcts import MCTS, TreeNode
import time
from typing import List
from constants import TIGER
from board import Board



def game_loop(board):
   
    board.show()
    count: int = 1
    mcts: MCTS = MCTS()
    
    
    # board play
    while True:
        print("Counter: ",count)
        board.ai = board.turn
        best_move: TreeNode = mcts.search(board)
        new_pos_list: List[int] = best_move.board.position
        move: str = board.get_move(board.position, new_pos_list)


        print(f"{'Tiger' if board.turn == TIGER else 'Goat'}", move)
        board = board.make_move(move)
        board.prev_moves.append(move)
        board.show()
        count += 1
        # print(board.prev_moves)
        
        if board.is_draw():
            print("Game drawn")
            break

        if board.is_win():
            print(f"{'Tiger' if -board.turn == TIGER else 'Goat'} win the game")
            break



if __name__ == '__main__':
    board = Board()
    game_loop(board)
    

