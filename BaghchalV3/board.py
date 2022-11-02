from copy import deepcopy
from collections import deque, Counter
from typing import Deque, List, Optional, Set
from constants import *


MAX_SIZE = 12

class Board:

    def __init__(self, board:'Board' = None) -> None:
        self.turn: int = GOAT
        self.position: List[int] = INITIAL_BOARD_POSITION
        self.goat_left_to_placed: int = 20
        self.goat_captured: int = 0
        self.tiger_trapped: int = 0
        self.is_goat_captured: bool = False 
        self.is_tiger_trapped: bool = False 
        self.is_goat_safe: bool = True 
        self.reward = 0 # new
        self.ai: Optional[int] = None
        self.level: int = 0
        self.prev_moves: Deque = deque(maxlen=MAX_SIZE)

        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    @staticmethod
    def parse_move(move: str) -> int:
        return int(move[1:]) if move.startswith("0") else int(move)

    def get_move(self, prev_pos_list: List[int], new_pos_list: List[int]) -> str:
        prev_pos_set: Set = set([ind for ind, pos in enumerate(prev_pos_list) if pos == self.ai])
        new_pos_set: Set = set([ind for ind, pos in enumerate(new_pos_list) if pos == self.ai])

        if self.ai == GOAT and self.goat_left_to_placed > 0:
            _to: int = list(new_pos_set - prev_pos_set)[0]
            _to_str: str = f"0{_to}" if _to < 10 else str(_to)
            return f"G{_to_str}"

        _from: int = list(prev_pos_set - new_pos_set)[0]
        _to: int = list(new_pos_set - prev_pos_set)[0]

        _from_str: str = f"0{_from}" if _from < 10 else str(_from)
        _to_str: str = f"0{_to}" if _to < 10 else str(_to)

        return f"B{_from_str}{_to_str}" if self.ai == TIGER else f"G{_from_str}{_to_str}"

    @staticmethod
    def show_pos(pos: int, ind: int) -> str:
        if pos == TIGER:
            return f"TT"
        elif pos == GOAT:
            return f"GG"
        else:
            return f"{ind}" if ind > 9 else f"0{ind}"


    def can_captured(self, _from: int, _to: int) -> bool:
        if self.position[_from] == TIGER and self.position[_to] == EMPTY:
            return (_to in CAPTUREDMOVES.get(_from)) and (self.position[int((_to + _from) / 2)] == GOAT)
        return False


    def get_tiger_pos(self) -> List[int]:
        return [ind for ind, pos in enumerate(self.position) if pos == TIGER]

    
    def get_goat_pos(self) -> List[int]:
        return [ind for ind, pos in enumerate(self.position) if pos == GOAT]


    def no_of_tiger_trapped(self) -> int:
        count: int = 0
        tiger_pos_list: List[int] = self.get_tiger_pos()
        for pos in tiger_pos_list:
            adj_move_list: List[int] = [idx for idx in LEGALMOVES.get(pos) if self.position[idx] == EMPTY]
            captured_move_list: List[int] = [idx for idx in CAPTUREDMOVES.get(pos) if
                                  (self.position[int((pos + idx) / 2)] == GOAT
                                   and self.position[idx] == EMPTY)]
            new_list: List[int] = adj_move_list + captured_move_list

            if len(new_list) == 0:
                count += 1

        return count


    def is_valid_move(self, move: str) -> bool:
        if len(move) == 3:
            _to: int = Board.parse_move(move[1:])
            return self.position[_to] == EMPTY

        elif len(move) == 5 and move.startswith("G"):
            _from: int = Board.parse_move(move[1:3])
            _to: int = Board.parse_move(move[3:5])

            return self.position[_from] == GOAT and self.position[_to] == EMPTY

        elif len(move) == 5 and move.startswith("B"):
            _from: int = Board.parse_move(move[1:3])
            _to: int = Board.parse_move(move[3:5])
            # check whether it is captured move
            if _to in CAPTUREDMOVES.get(_from):
                return self.can_captured(_from, _to)

            return self.position[_from] == TIGER and self.position[_to] == EMPTY

        else:
            return False


    def check_goat_safe(self) -> bool:
        tiger_curr_pos: List[int] = self.get_tiger_pos()
        for pos in tiger_curr_pos:
            captured_moves = CAPTUREDMOVES.get(pos)
            for c_move in captured_moves:
                if self.can_captured(pos, c_move):
                    return False
        return True


    def make_move(self, move: str) -> 'Board':
        new_board:Board = Board(self)

        if len(move) == 3:
            _to: int = Board.parse_move(move[1:])
            new_board.position[_to] = GOAT
            new_board.goat_left_to_placed -= 1
            new_board.is_tiger_trapped = new_board.tiger_trapped < new_board.no_of_tiger_trapped()
            new_board.tiger_trapped = new_board.no_of_tiger_trapped()
            new_board.is_goat_safe = new_board.check_goat_safe()
            new_board.reward = 20 if (new_board.tiger_trapped and new_board.is_goat_safe) else 10 if new_board.is_goat_safe else 0

        elif len(move) == 5 and move.startswith("G"):
            _from: int = Board.parse_move(move[1:3])
            _to: int = Board.parse_move(move[3:5])
            new_board.position[_from] = 0
            new_board.position[_to] = GOAT
            new_board.is_tiger_trapped = new_board.tiger_trapped <= new_board.no_of_tiger_trapped()
            new_board.tiger_trapped = new_board.no_of_tiger_trapped()
            new_board.is_goat_safe = new_board.check_goat_safe()
            new_board.reward = 20 if (new_board.tiger_trapped and new_board.is_goat_safe) else 10 if new_board.is_goat_safe else 0

        elif len(move) == 5 and move.startswith("B"):
            _from: int = Board.parse_move(move[1:3])
            _to: int = Board.parse_move(move[3:5])

            if new_board.can_captured(_from, _to):
                new_board.position[int((_from + _to) / 2)] = 0
                new_board.goat_captured += 1
                new_board.is_goat_captured = True

            new_board.position[_from] = 0
            new_board.position[_to] = TIGER
            new_board.reward = 20 if new_board.is_goat_captured else 0

        new_board.turn = - new_board.turn
        return new_board


    def is_draw(self) -> bool:
        return (
            (self.goat_captured == 5 and self.tiger_trapped == 4) or 
            (len(self.prev_moves) == MAX_SIZE and (Counter(self.prev_moves).most_common(1)[0][1] == MAX_SIZE/4 and self.goat_left_to_placed == 0))
        )


    def is_win(self) -> bool:
        if self.turn == - TIGER and self.goat_captured == 5:
            return True
        elif self.turn == - GOAT and self.tiger_trapped == 4:
            return True
        else:
            return False

    def generate_possible_moves(self) -> List['Board']:
        move_list: List['Board'] = []
        if self.turn == TIGER:
            tiger_pos_list: List[int] = self.get_tiger_pos()
            for pos in tiger_pos_list:
                moves: List[int] = LEGALMOVES.get(pos) + CAPTUREDMOVES.get(pos)
                for move in moves:
                    from_str = f"0{pos}" if pos < 10 else str(pos)
                    to_str = f"0{move}" if move < 10 else str(move)
                    move_str = f"B{from_str}{to_str}"
                    if self.is_valid_move(move_str):
                        move_list.append(self.make_move(move_str))

        elif self.turn == GOAT and self.goat_left_to_placed > 0:
            empty_pos: List[int] = [ind for ind, pos in enumerate(self.position) if pos == EMPTY]
            move_list = [self.make_move(f"G0{pos}") if pos < 10 else self.make_move(f"G{pos}") for pos in empty_pos]

        elif self.turn == GOAT and self.goat_left_to_placed == 0:
            goat_pos_list: List[int] = self.get_goat_pos()
            for pos in goat_pos_list:
                moves = LEGALMOVES.get(pos)
                for move in moves:
                    from_str = f"0{pos}" if pos < 10 else str(pos)
                    to_str = f"0{move}" if move < 10 else str(move)
                    move_str = f"G{from_str}{to_str}"
                    if self.is_valid_move(move_str):
                        move_list.append(self.make_move(move_str))
           
        return move_list


    def show(self):

        print("""  a   b   c   d   e
1 %s   %s   %s   %s   %s
  | \\ | / | \\ | / |
2 %s   %s   %s   %s   %s
  | / | \\ | / | \\ |
3 %s   %s   %s   %s   %s
  | \\ | / | \\ | / |
4 %s   %s   %s   %s   %s
  | / | \\ | / | \\ |
5 %s   %s   %s   %s   %s\n""" % tuple(Board.show_pos(pos, ind) for ind, pos in enumerate(self.position)))
        print("Turn: %s" % ("Goat" if self.turn == GOAT else "Tiger"))
        print("Remaining Goats to place: %d/20" % self.goat_left_to_placed)
        print("Dead Goats: %d" % self.goat_captured)
        print("Tiger Trapped: %d\n" % self.tiger_trapped)

    