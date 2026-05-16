import time
import config
from board import Board
from ai import AI

def parse_board(board, board_layout):
    for r in range(config.BOARD_SIZE):
        for c in range(config.BOARD_SIZE):
            char = board_layout[r][c]
            if char == 'X':
                board.state[r][c] = config.PLAYER_X
            elif char == 'O':
                board.state[r][c] = config.PLAYER_O
            else:
                board.state[r][c] = config.EMPTY

def run_test_case(test_name, board_layout, depth):
    print(f"\n{'='*50}")
    print(f"TEST CASE: {test_name} (Độ sâu: {depth})")
    print(f"{'='*50}")
    
    # 1. Chạy Minimax
    board_mm = Board()
    parse_board(board_mm, board_layout)
    ai_mm = AI(board_mm)
    
    start_time = time.time()
    best_move_mm, score_mm = ai_mm.minimax(depth, True)
    time_mm = time.time() - start_time
    nodes_mm = ai_mm.nodes_explored
    
    # 2. Chạy Alpha-Beta
    board_ab = Board()
    parse_board(board_ab, board_layout)
    ai_ab = AI(board_ab)
    
    start_time = time.time()
    best_move_ab, score_ab = ai_ab.alphabeta(depth, -float('inf'), float('inf'), True)
    time_ab = time.time() - start_time
    nodes_ab = ai_ab.nodes_explored
    
    # 3. In kết quả so sánh
    print(f"{'Thuật toán':<15} | {'Nước đi':<10} | {'Số node đã xét':<15} | {'Thời gian (s)':<15}")
    print("-" * 65)
    print(f"{'Minimax':<15} | {str(best_move_mm):<10} | {nodes_mm:<15} | {time_mm:.4f}")
    print(f"{'Alpha-Beta':<15} | {str(best_move_ab):<10} | {nodes_ab:<15} | {time_ab:.4f}")
    
    # Tính phần trăm tối ưu
    if nodes_mm > 0:
        saved_percent = ((nodes_mm - nodes_ab) / nodes_mm) * 100
        print(f"Alpha-Beta đã giảm được {saved_percent:.2f}% số trạng thái cần xét!")

def main():
    
    test_1 = [
        ".........",
        ".........",
        ".........",
        ".........",
        "....X....",
        ".........",
        ".........",
        ".........",
        "........."
    ]
    
    test_2 = [
        ".........",
        ".........",
        ".........",
        "....X....",
        "....X....",
        "....X....",
        ".........",
        ".........",
        "........."
    ] # Người (X) có 3 quân, AI (O) bắt buộc phải chặn 2 đầu
    
    test_3 = [
        ".........",
        ".........",
        ".........",
        "....O....",
        "....O....",
        "....O....",
        ".........",
        ".........",
        "........."
    ] # AI (O) có 3 quân, AI cần tấn công để thắng ngay
    
    test_4 = [
        ".........",
        ".........",
        "....X....",
        "...OX....",
        "...XOO...",
        "....X....",
        ".........",
        ".........",
        "........."
    ] # Trạng thái giữa ván, xen kẽ tấn công và phòng thủ
    
    test_5 = [
        "X.O.X.O..",
        ".X.O.X.O.",
        "O.X.O.X..",
        ".O.X.O.X.",
        "X.O.X.O..",
        ".........",
        ".........",
        ".........",
        "........."
    ] # Trạng thái rất nhiều nước cờ phân tán, test khả năng cắt nhánh
    
    # Lượt đi tiếp theo luôn giả định là của AI (Tìm Max)
    run_test_case("1. Trạng thái đầu ván", test_1, depth=2)
    run_test_case("2. AI cần chặn người chơi", test_2, depth=2)
    run_test_case("3. AI tấn công để thắng", test_3, depth=2)
    run_test_case("4. Trạng thái giữa ván", test_4, depth=2)
    run_test_case("5. Trạng thái phân tán phức tạp", test_5, depth=2)

if __name__ == "__main__":
    main()