import math
import config

class AI:
    def __init__(self, board):
        self.board = board
        self.nodes_explored = 0

    def evaluate_window(self, window, player):
        # Đánh giá điểm của 1 cửa sổ gồm 4 ô liên tiếp.
        score = 0
        opponent = config.PLAYER_X if player == config.PLAYER_O else config.PLAYER_O
        
        player_count = window.count(player)
        empty_count = window.count(config.EMPTY)
        opponent_count = window.count(opponent)
        
        # Điểm thưởng cho AI (Max)
        if player_count == 4:
            score += 100000
        elif player_count == 3 and empty_count == 1:
            score += 1000
        elif player_count == 2 and empty_count == 2:
            score += 100
            
        # Điểm phạt nếu người chơi (Min) sắp thắng (Phải ưu tiên chặn)
        if opponent_count == 4:
            score -= 100000
        elif opponent_count == 3 and empty_count == 1:
            score -= 10000  
        elif opponent_count == 2 and empty_count == 2:
            score -= 100
            
        return score

    def evaluate_state(self, player):
        # Quét toàn bộ bàn cờ để tính tổng điểm trạng thái hiện tại.
        score = 0
        size = config.BOARD_SIZE
        state = self.board.state
        
        # Quét hàng ngang
        for r in range(size):
            for c in range(size - 3):
                window = list(state[r, c:c+4])
                score += self.evaluate_window(window, player)
                
        # Quét hàng dọc
        for c in range(size):
            for r in range(size - 3):
                window = [state[r+i][c] for i in range(4)]
                score += self.evaluate_window(window, player)
                
        # Quét chéo xuống phải (\)
        for r in range(size - 3):
            for c in range(size - 3):
                window = [state[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window, player)
                
        # Quét chéo xuống trái (/)
        for r in range(size - 3):
            for c in range(3, size):
                window = [state[r+i][c-i] for i in range(4)]
                score += self.evaluate_window(window, player)
                
        return score

    def minimax(self, depth, maximizingPlayer):
        self.nodes_explored += 1
        is_terminal, winner = self.board.check_terminal()
        
        # Điều kiện dừng: Chạm đáy độ sâu hoặc ván cờ kết thúc
        if depth == 0 or is_terminal:
            if is_terminal:
                if winner == config.PLAYER_O: return None, 10000000
                elif winner == config.PLAYER_X: return None, -10000000
                else: return None, 0
            else:
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
        else:
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
                if winner == config.PLAYER_O: return None, 10000000
                elif winner == config.PLAYER_X: return None, -10000000
                else: return None, 0
            else:
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
        else:
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