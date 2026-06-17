import math
import random
import time
from dataclasses import dataclass

from .. import config


@dataclass(frozen=True)
class SearchResult:
    move: tuple[int, int] | None
    score: float
    depth: int
    nodes_explored: int
    elapsed_sec: float
    algorithm: str


class Agent:
    def __init__(self, board):
        self.board = board
        self.nodes_explored = 0

    def evaluate_window(self, window, player):
        score = 0
        opponent = config.PLAYER_X if player == config.PLAYER_O else config.PLAYER_O

        player_count = window.count(player)
        empty_count = window.count(config.EMPTY)
        opponent_count = window.count(opponent)

        if player_count == 4:
            score += 100000
        elif player_count == 3 and empty_count == 1:
            score += 1000
        elif player_count == 2 and empty_count == 2:
            score += 100

        if opponent_count == 4:
            score -= 100000
        elif opponent_count == 3 and empty_count == 1:
            score -= 10000
        elif opponent_count == 2 and empty_count == 2:
            score -= 100

        return score

    def evaluate_state(self, player):
        score = 0
        size = config.BOARD_SIZE
        state = self.board.state

        for r in range(size):
            for c in range(size - 3):
                score += self.evaluate_window(list(state[r, c:c + 4]), player)

        for c in range(size):
            for r in range(size - 3):
                score += self.evaluate_window([state[r + i][c] for i in range(4)], player)

        for r in range(size - 3):
            for c in range(size - 3):
                score += self.evaluate_window([state[r + i][c + i] for i in range(4)], player)

        for r in range(size - 3):
            for c in range(3, size):
                score += self.evaluate_window([state[r + i][c - i] for i in range(4)], player)

        return score

    def _opening_move(self):
        valid_moves = self.board.get_valid_moves()
        if not valid_moves:
            return None, 0
        return random.choice(valid_moves), 0

    def search_minimax(self, depth, maximizingPlayer=True):
        self.nodes_explored = 0
        start_time = time.time()
        move, score = self.minimax(depth, maximizingPlayer)
        return SearchResult(move, score, depth, self.nodes_explored, time.time() - start_time, "Minimax")

    def search_alphabeta(self, depth, alpha=-math.inf, beta=math.inf, maximizingPlayer=True):
        self.nodes_explored = 0
        start_time = time.time()
        move, score = self.alphabeta(depth, alpha, beta, maximizingPlayer)
        return SearchResult(move, score, depth, self.nodes_explored, time.time() - start_time, "Alpha-Beta")

    def minimax(self, depth, maximizingPlayer):
        self.nodes_explored += 1
        is_terminal, winner = self.board.check_terminal()

        if depth == 0 or is_terminal:
            if is_terminal:
                if winner == config.PLAYER_O:
                    return None, 10000000
                if winner == config.PLAYER_X:
                    return None, -10000000
                return None, 0
            if self.nodes_explored == 1 and not self.board.state.any():
                return self._opening_move()
            return None, self.evaluate_state(config.PLAYER_O)

        valid_moves = self.board.get_valid_moves()
        best_move = valid_moves[0] if valid_moves else None

        if maximizingPlayer:
            max_eval = -math.inf
            for move in valid_moves:
                self.board.make_move(move[0], move[1], config.PLAYER_O)
                _, eval_score = self.minimax(depth - 1, False)
                self.board.undo_move(move[0], move[1])

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            return best_move, max_eval

        min_eval = math.inf
        for move in valid_moves:
            self.board.make_move(move[0], move[1], config.PLAYER_X)
            _, eval_score = self.minimax(depth - 1, True)
            self.board.undo_move(move[0], move[1])

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return best_move, min_eval

    def alphabeta(self, depth, alpha, beta, maximizingPlayer):
        self.nodes_explored += 1
        is_terminal, winner = self.board.check_terminal()

        if depth == 0 or is_terminal:
            if is_terminal:
                if winner == config.PLAYER_O:
                    return None, 10000000
                if winner == config.PLAYER_X:
                    return None, -10000000
                return None, 0
            if self.nodes_explored == 1 and not self.board.state.any():
                return self._opening_move()
            return None, self.evaluate_state(config.PLAYER_O)

        valid_moves = self.board.get_valid_moves()
        best_move = valid_moves[0] if valid_moves else None

        if maximizingPlayer:
            max_eval = -math.inf
            for move in valid_moves:
                self.board.make_move(move[0], move[1], config.PLAYER_O)
                _, eval_score = self.alphabeta(depth - 1, alpha, beta, False)
                self.board.undo_move(move[0], move[1])

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return best_move, max_eval

        min_eval = math.inf
        for move in valid_moves:
            self.board.make_move(move[0], move[1], config.PLAYER_X)
            _, eval_score = self.alphabeta(depth - 1, alpha, beta, True)
            self.board.undo_move(move[0], move[1])

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return best_move, min_eval


AI = Agent
