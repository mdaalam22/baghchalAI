from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
# import uvicorn
import numpy as np

from board import Board
from mcts import MCTS

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
    mcts  = MCTS()
    

    board.position = np.array(data.position)
    board.goat_left_to_placed = data.goat_left_to_placed
    board.goat_captured = data.goat_captured
    board.level = data.level
    board.ai = data.ai
    board.turn = data.ai

    best_move = mcts.search(board)
    # best_moves = board.generate_possible_moves() # new
    # best_move = max(best_moves, key = lambda obj: obj.reward) # new
    # new_pos_list = best_move.position # new

    new_pos_list = best_move.board.position

    move = board.get_move(data.position, new_pos_list)
    print(move)
    print(best_move.board.reward)
    return {'success': True, 'move': move}



# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=3000)
   
