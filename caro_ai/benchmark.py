import json
import os
import time

from . import config
from .ai import Agent
from .game import Board


def parse_board(board, board_layout):
    for r in range(config.BOARD_SIZE):
        for c in range(config.BOARD_SIZE):
            char = board_layout[r][c]
            if char == "X":
                board.state[r][c] = config.PLAYER_X
            elif char == "O":
                board.state[r][c] = config.PLAYER_O
            else:
                board.state[r][c] = config.EMPTY


def run_test_case(test_name, board_layout, depth):
    print(f"\n{'=' * 50}")
    print(f"TEST CASE: {test_name} (Độ sâu: {depth})")
    print(f"{'=' * 50}")

    board_mm = Board()
    parse_board(board_mm, board_layout)
    ai_mm = Agent(board_mm)

    result_mm = ai_mm.search_minimax(depth, True)

    board_ab = Board()
    parse_board(board_ab, board_layout)
    ai_ab = Agent(board_ab)

    result_ab = ai_ab.search_alphabeta(depth, -float("inf"), float("inf"), True)

    print(f"{'Thuật toán':<15} | {'Nước đi':<10} | {'Giá trị':<10} | {'Độ sâu':<7} | {'Node':<10} | {'Thời gian (s)':<15}")
    print("-" * 84)
    print(f"{result_mm.algorithm:<15} | {str(result_mm.move):<10} | {result_mm.score:<10} | {result_mm.depth:<7} | {result_mm.nodes_explored:<10} | {result_mm.elapsed_sec:.4f}")
    print(f"{result_ab.algorithm:<15} | {str(result_ab.move):<10} | {result_ab.score:<10} | {result_ab.depth:<7} | {result_ab.nodes_explored:<10} | {result_ab.elapsed_sec:.4f}")

    if result_mm.nodes_explored > 0:
        saved_percent = ((result_mm.nodes_explored - result_ab.nodes_explored) / result_mm.nodes_explored) * 100
        print(f"Alpha-Beta đã giảm được {saved_percent:.2f}% số trạng thái cần xét!")


def main():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "benchmark_config.json")
    if not os.path.exists(config_path):
        print(f"Benchmark config not found: {config_path}")
        return 1

    with open(config_path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)

    boards = payload.get("boards") or []
    if not boards:
        boards = [
            {
                "name": "1. Trạng thái đầu ván",
                "layout": [
                    ".........",
                    ".........",
                    ".........",
                    ".........",
                    "....X....",
                    ".........",
                    ".........",
                    ".........",
                    ".........",
                ],
                "depth": 2,
            },
            {
                "name": "2. AI cần chặn người chơi",
                "layout": [
                    ".........",
                    ".........",
                    ".........",
                    "....X....",
                    "....X....",
                    "....X....",
                    ".........",
                    ".........",
                    ".........",
                ],
                "depth": 2,
            },
            {
                "name": "3. AI tấn công để thắng",
                "layout": [
                    ".........",
                    ".........",
                    ".........",
                    "....O....",
                    "....O....",
                    "....O....",
                    ".........",
                    ".........",
                    ".........",
                ],
                "depth": 2,
            },
        ]

    for item in boards:
        run_test_case(item["name"], item["layout"], depth=int(item.get("depth", 2)))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
