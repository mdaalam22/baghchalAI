from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

from board import Board
from mcts import MCTS
import play_nn

app = FastAPI()

class BoardSchema(BaseModel):
    position: List[int]
    goat_left_to_placed: int
    goat_captured: int
    tiger_trapped: int
    level: int
    ai: int

@app.get('/api')
async def root():
    return {"message": "Hello World"}

@app.post('/api/get-move')
async def get_move(data: BoardSchema) -> str:

    board = Board()
    board.position = np.array(data.position)
    board.goat_left_to_placed = data.goat_left_to_placed
    board.goat_captured = data.goat_captured
    board.level = data.level
    board.ai = data.ai
    board.turn = data.ai

    mcts  = MCTS(board.level)

    if board.level == 3:
        best_moves = board.generate_possible_moves()
        best_move = play_nn.best_move_nn(board, best_moves)
        new_pos_list = best_move.position 
        move: str = board.get_move(board.position, new_pos_list)
        return {'success': True, 'move': move}

    best_move = mcts.search(board)

    new_pos_list = best_move.board.position

    move = board.get_move(data.position, new_pos_list)
    print(move)
    print(best_move.board.reward)
    return {'success': True, 'move': move}


   
