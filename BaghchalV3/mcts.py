import math
import random
from typing import List, Optional
from board import Board
from constants import GOAT, TIGER

class TreeNode:

    def __init__(self, board: Board, parent: 'TreeNode') -> None:

        self.board = board
        self.is_terminal = self.board.is_win() or self.board.is_draw()
        self.is_fully_expanded = self.is_terminal
        self.parent = parent
        self.visits = 0
        self.score = 0
        self.children = {}


class MCTS:

    def __init__(self):
        self.root: Optional[TreeNode] = None

    def search(self, initial_state: Board) -> TreeNode:
        self.root = TreeNode(initial_state, None)

        for iteration in range(500):
            # selection phase
            node: TreeNode = self.select(self.root)

            # simulation phase
            score: int = 0 if node is None else self.rollout(node.board)

            # backpropagation
            self.backpropagate(node, score)

        try:
            return self.get_best_move(self.root, 0)
        except:
            pass

    def select(self, node: TreeNode) -> TreeNode:
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_move(node, 2)
            else:
                return self.expand(node)
        return node


    def expand(self, node: TreeNode) ->  TreeNode:
        states: Board = node.board.generate_possible_moves()
        for state in states:
            key_str: str = str(state.position)
            if f"{key_str}" not in node.children:
                new_node: TreeNode = TreeNode(state, node)
                node.children[f"{key_str}"] = new_node
                if len(states) == len(node.children):
                    node.is_fully_expanded = True
                return new_node
            # return node
        print("not here")


    def rollout(self, board: Board) -> int:
        while not (board.is_win() or board.is_draw()):
            try:
                # board = random.choice(board.generate_possible_moves())
                board = max(board.generate_possible_moves, key = lambda obj: obj.reward)
            except:
                return 0
    
        if board.turn == board.ai:
            return 1
        return -1

    def backpropagate(self, node: TreeNode, score: int):
        while node is not None:
            node.visits += 1
            node.score += score
            node = node.parent


    def get_best_move_by_policy(self, best_moves: TreeNode, turn: int) -> TreeNode:
        if len(best_moves) == 1:
            # print("*********best moves only 1**********")
            return best_moves[0]
        elif turn == TIGER or turn == GOAT:
            move_list: List[bool] = [move.board.is_goat_captured if turn == TIGER else (move.board.is_goat_safe and move.board.is_tiger_trapped) or move.board.is_goat_safe for move in best_moves]
            if any(move_list):
                idx = random.choice(list(filter(lambda x: move_list[x], range(len(move_list)))))
                return best_moves[idx]
            return random.choice(best_moves)
        else:
            return random.choice(best_moves)



    def get_best_move(self, node: TreeNode, exploration_constant: int) -> TreeNode:
        best_score: float = float('-inf')
        best_moves: List[TreeNode] = []
        for child_node in node.children.values():
            if child_node.board.turn == node.board.ai:
                current_player: int = 1
            else:
                current_player: int = -1

            # get move score using UCT formula
            move_score: float = current_player * child_node.score / child_node.visits + math.sqrt(exploration_constant) * math.sqrt(
                math.log(node.visits) / child_node.visits)

            if move_score > best_score:
                best_score = move_score
                best_moves = [child_node]
                # best_moves.append(child_node)

            elif move_score == best_score:
                best_moves.append(child_node)
        # return random.choice(best_moves)
        return self.get_best_move_by_policy(best_moves, -best_moves[0].board.turn)
