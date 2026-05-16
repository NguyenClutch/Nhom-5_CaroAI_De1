import time
import config
from board import Board
from ai import AI

def print_board(board):
    chars = {config.EMPTY: '.', config.PLAYER_X: 'X', config.PLAYER_O: 'O'}
    print("\n   " + " ".join([str(i) for i in range(config.BOARD_SIZE)]))
    for r in range(config.BOARD_SIZE):
        row_str = f"{r}  " + " ".join([chars[board.state[r][c]] for c in range(config.BOARD_SIZE)])
        print(row_str)
    print()

def main():
    board = Board()
    ai = AI(board)
    
    print("="*30)
    print(" TRÒ CHƠI CỜ CARO AI ")
    print("Bạn là X, AI là O. Bạn đi trước.")
    print("="*30)
    
    algo_choice = input("Chọn thuật toán AI (1: Minimax, 2: Alpha-Beta): ")
    use_alphabeta = (algo_choice == '2')
    
    # Gợi ý: Với Minimax thường chỉ nên chạy độ sâu 2 trên bàn 9x9 vì cực kỳ chậm.
    # Với Alpha-beta có thể chạy độ sâu 3 hoặc 4.
    depth = int(input("Nhập độ sâu tìm kiếm (Depth): "))
    
    current_player = config.PLAYER_X
    
    while True:
        print_board(board)
        is_terminal, winner = board.check_terminal()
        if is_terminal:
            if winner == config.PLAYER_X:
                print("Chúc mừng! Bạn đã thắng!")
            elif winner == config.PLAYER_O:
                print("AI đã thắng! Chúc bạn may mắn lần sau.")
            else:
                print("Trò chơi kết thúc với kết quả Hòa!")
            break
            
        if current_player == config.PLAYER_X:
            while True:
                try:
                    move_str = input("Nhập nước đi của bạn (row col) vd '4 4': ")
                    r, c = map(int, move_str.split())
                    if 0 <= r < config.BOARD_SIZE and 0 <= c < config.BOARD_SIZE:
                        if board.make_move(r, c, config.PLAYER_X):
                            break
                        else:
                            print("Ô này đã có người đánh. Chọn ô khác.")
                    else:
                        print("Tọa độ vượt quá bàn cờ.")
                except ValueError:
                    print("Vui lòng nhập đúng định dạng, cách nhau bởi khoảng trắng.")
                    
            current_player = config.PLAYER_O
        else:
            print("\nAI đang suy nghĩ...")
            ai.nodes_explored = 0
            start_time = time.time()
            
            if use_alphabeta:
                best_move, score = ai.alphabeta(depth, -float('inf'), float('inf'), True)
            else:
                best_move, score = ai.minimax(depth, True)
                
            end_time = time.time()
            
            if best_move:
                board.make_move(best_move[0], best_move[1], config.PLAYER_O)
                print(f"AI đánh vào ô: {best_move[0]} {best_move[1]}")
                print(f"Điểm đánh giá: {score}")
                print(f"Số trạng thái đã xét: {ai.nodes_explored}")
                print(f"Thời gian chạy: {end_time - start_time:.4f} giây")
            
            current_player = config.PLAYER_X

if __name__ == "__main__":
    main()