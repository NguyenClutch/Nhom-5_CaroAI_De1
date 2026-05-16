import numpy as np
import config

class Board:
    def __init__(self):
        # Khởi tạo bàn cờ với kích thước từ config, gán toàn bộ là ô trống (0)
        self.state = np.zeros((config.BOARD_SIZE, config.BOARD_SIZE), dtype=int)

    def get_valid_moves(self):
        moves = []
        for r in range(config.BOARD_SIZE):
            for c in range(config.BOARD_SIZE):
                if self.state[r][c] == config.EMPTY:
                    moves.append((r, c))
        return moves

    def make_move(self, row, col, player):
        if self.state[row][col] == config.EMPTY:
            self.state[row][col] = player
            return True
        return False
        
    def undo_move(self, row, col):
        self.state[row][col] = config.EMPTY

    def check_winner(self, player):
        size = config.BOARD_SIZE
        win_cond = config.WIN_CONDITION

        # Duyệt qua từng ô trên bàn cờ
        for r in range(size):
            for c in range(size):
                if self.state[r][c] == player:           
                    # 1. Kiểm tra hàng ngang 
                    if c + win_cond <= size:
                        if all(self.state[r][c + i] == player for i in range(win_cond)):
                            return True                           
                    # 2. Kiểm tra hàng dọc 
                    if r + win_cond <= size:
                        if all(self.state[r + i][c] == player for i in range(win_cond)):
                            return True                         
                    # 3. Kiểm tra đường chéo xuống dưới bên phải (\)
                    if r + win_cond <= size and c + win_cond <= size:
                        if all(self.state[r + i][c + i] == player for i in range(win_cond)):
                            return True               
                    # 4. Kiểm tra đường chéo xuống dưới bên trái (/)
                    if r + win_cond <= size and c - win_cond >= -1:
                        if all(self.state[r + i][c - i] == player for i in range(win_cond)):
                            return True
                            
        return False

    def is_draw(self):
        return not np.any(self.state == config.EMPTY)

    def check_terminal(self):
        if self.check_winner(config.PLAYER_X):
            return True, config.PLAYER_X
        if self.check_winner(config.PLAYER_O):
            return True, config.PLAYER_O
        if self.is_draw():
            return True, config.EMPTY  
        return False, None