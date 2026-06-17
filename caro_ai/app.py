import argparse
import json
import math
import os
import time

from . import config
from .ai import Agent
from .benchmark import main as benchmark_main
from .game import Board
from .modes import GameMode
from .ui import Button


def _get_repo_root():
    return os.path.dirname(os.path.dirname(__file__))


def _load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _create_font(pygame, size, bold=False):
    candidates = ["segoeui", "tahoma", "arial", "dejavusans", "notosans"]
    for family in candidates:
        font_path = pygame.font.match_font(family, bold=bold)
        if font_path:
            return pygame.font.Font(font_path, size)
    return pygame.font.Font(None, size)


def print_board(board):
    chars = {config.EMPTY: ".", config.PLAYER_X: "X", config.PLAYER_O: "O"}
    print("\n   " + " ".join([str(i) for i in range(config.BOARD_SIZE)]))
    for r in range(config.BOARD_SIZE):
        row_str = f"{r}  " + " ".join([chars[board.state[r][c]] for c in range(config.BOARD_SIZE)])
        print(row_str)
    print()


def _run_human_vs_ai():
    board = Board()
    ai = Agent(board)

    print("=" * 30)
    print(" TRÒ CHƠI CỜ CARO AI ")
    print("Bạn là X, AI là O. Bạn đi trước.")
    print("=" * 30)

    algo_choice = input("Chọn thuật toán AI (1: Minimax, 2: Alpha-Beta): ")
    ai_mode = "alphabeta" if algo_choice == "2" else "minimax"
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
                        print("Ô này đã có người đánh. Chọn ô khác.")
                    else:
                        print("Tọa độ vượt quá bàn cờ.")
                except ValueError:
                    print("Vui lòng nhập đúng định dạng, cách nhau bởi khoảng trắng.")

            current_player = config.PLAYER_O
            continue

        print("\nAI đang suy nghĩ...")
        search_result = ai.search_alphabeta(depth, -math.inf, math.inf, True) if ai_mode == "alphabeta" else ai.search_minimax(depth, True)

        if search_result.move:
            board.make_move(search_result.move[0], search_result.move[1], config.PLAYER_O)
            print(f"AI đánh vào ô: {search_result.move[0]} {search_result.move[1]}")
            print(f"Thuật toán: {search_result.algorithm}")
            print(f"Giá trị đánh giá: {search_result.score}")
            print(f"Độ sâu tìm kiếm: {search_result.depth}")
            print(f"Số trạng thái đã xét: {search_result.nodes_explored}")
            print(f"Thời gian chạy: {search_result.elapsed_sec:.4f} giây")

        current_player = config.PLAYER_X


def _run_ai_vs_ai(depth=2):
    board = Board()
    ai = Agent(board)
    current_player = config.PLAYER_X

    print("=" * 30)
    print(" CHẾ ĐỘ DEVELOPER: AI VS AI ")
    print("X đi trước, cả hai phía dùng Alpha-Beta.")
    print("=" * 30)

    while True:
        print_board(board)
        is_terminal, winner = board.check_terminal()
        if is_terminal:
            if winner == config.PLAYER_X:
                print("AI X đã thắng!")
            elif winner == config.PLAYER_O:
                print("AI O đã thắng!")
            else:
                print("Ván đấu kết thúc với kết quả hòa.")
            break

        ai.nodes_explored = 0
        start_time = time.time()
        if current_player == config.PLAYER_X:
            best_move, score = ai.minimax(depth, False)
        else:
            best_move, score = ai.alphabeta(depth, -math.inf, math.inf, True)
        elapsed = time.time() - start_time

        if best_move:
            board.make_move(best_move[0], best_move[1], current_player)
            print(f"Nước đi: {best_move} | điểm: {score} | node: {ai.nodes_explored} | {elapsed:.4f}s")

        current_player = config.PLAYER_O if current_player == config.PLAYER_X else config.PLAYER_X


def _draw_grid(screen, board, font, status_text):
    import pygame

    screen.fill((18, 20, 28))
    board_rect = pygame.Rect(30, 30, 540, 540)
    pygame.draw.rect(screen, (232, 230, 225), board_rect, border_radius=16)

    cell_size = board_rect.width // config.BOARD_SIZE
    for idx in range(config.BOARD_SIZE + 1):
        x = board_rect.left + idx * cell_size
        y = board_rect.top + idx * cell_size
        pygame.draw.line(screen, (45, 50, 60), (x, board_rect.top), (x, board_rect.bottom), 2)
        pygame.draw.line(screen, (45, 50, 60), (board_rect.left, y), (board_rect.right, y), 2)

    for r in range(config.BOARD_SIZE):
        for c in range(config.BOARD_SIZE):
            center_x = board_rect.left + c * cell_size + cell_size // 2
            center_y = board_rect.top + r * cell_size + cell_size // 2
            if board.state[r][c] == config.PLAYER_X:
                pygame.draw.line(screen, (40, 110, 220), (center_x - 16, center_y - 16), (center_x + 16, center_y + 16), 4)
                pygame.draw.line(screen, (40, 110, 220), (center_x + 16, center_y - 16), (center_x - 16, center_y + 16), 4)
            elif board.state[r][c] == config.PLAYER_O:
                pygame.draw.circle(screen, (210, 70, 70), (center_x, center_y), 18, 4)

    label = font.render(status_text, True, (236, 239, 245))
    screen.blit(label, (30, 580))

    return board_rect


def _draw_button(screen, button_font, button, active=False):
    import pygame

    base_color = (68, 78, 96) if not active else (74, 125, 232)
    border_color = (108, 120, 142) if not active else (160, 190, 255)
    text_color = (246, 247, 250)
    pygame.draw.rect(screen, base_color, button.rect, border_radius=12)
    pygame.draw.rect(screen, border_color, button.rect, width=2, border_radius=12)
    label = button_font.render(button.label, True, text_color)
    label_rect = label.get_rect(center=button.rect.center)
    screen.blit(label, label_rect)


def _move_count(board):
    return int((board.state != config.EMPTY).sum())


def _reset_game(mode):
    board = Board()
    ai = Agent(board)
    return {
        "board": board,
        "ai": ai,
        "mode": mode,
        "ai_mode": mode,
        "current_player": config.PLAYER_X,
        "game_over": False,
        "winner": None,
        "status_text": "Chọn chế độ chơi rồi bắt đầu đánh.",
    }


def _apply_move(state, row, col, player):
    if not state["board"].make_move(row, col, player):
        return False

    is_terminal, winner = state["board"].check_terminal()
    if is_terminal:
        state["game_over"] = True
        state["winner"] = winner
        if winner == config.EMPTY:
            state["status_text"] = "Ván đấu kết thúc hòa."
        elif winner == config.PLAYER_X:
            state["status_text"] = "X đã thắng."
        else:
            state["status_text"] = "O đã thắng."
    else:
        state["current_player"] = config.PLAYER_O if player == config.PLAYER_X else config.PLAYER_X
        state["status_text"] = "Đến lượt " + ("X" if state["current_player"] == config.PLAYER_X else "O")
    return True


def _run_pygame_ui():
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((660, 800))
    pygame.display.set_caption("Caro AI")
    font = _create_font(pygame, 22)
    button_font = _create_font(pygame, 20)
    clock = pygame.time.Clock()

    mode_labels = {
        "human_human": "Người - Người",
        "human_ai": "Người - Máy",
        "ai_ai": "Máy - Máy",
    }
    state = _reset_game("human_ai")

    buttons = [
        Button("Người - Người", "set_mode_human_human", pygame.Rect(30, 600, 160, 34)),
        Button("Người - Máy", "set_mode_human_ai", pygame.Rect(200, 600, 140, 34)),
        Button("Máy - Máy", "set_mode_ai_ai", pygame.Rect(350, 600, 120, 34)),
        Button("Minimax", "set_ai_minimax", pygame.Rect(30, 642, 100, 30)),
        Button("Alpha-Beta", "set_ai_alphabeta", pygame.Rect(140, 642, 110, 30)),
        Button("Chơi lại", "replay", pygame.Rect(30, 684, 100, 32)),
        Button("Thoát", "quit", pygame.Rect(140, 684, 90, 32)),
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_button = None
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        clicked_button = button
                        break

                if clicked_button is not None:
                    if clicked_button.action == "quit":
                        pygame.quit()
                        return 0
                    if clicked_button.action == "replay":
                        state = _reset_game(state["mode"])
                    elif clicked_button.action == "set_mode_human_human":
                        state = _reset_game("human_human")
                    elif clicked_button.action == "set_mode_human_ai":
                        state = _reset_game("human_ai")
                        state["ai_mode"] = "alphabeta"
                    elif clicked_button.action == "set_mode_ai_ai":
                        state = _reset_game("ai_ai")
                    elif clicked_button.action == "set_ai_minimax":
                        state["ai_mode"] = "minimax"
                        state["status_text"] = "AI: Minimax"
                    elif clicked_button.action == "set_ai_alphabeta":
                        state["ai_mode"] = "alphabeta"
                        state["status_text"] = "AI: Alpha-Beta"
                    continue

                board_rect = pygame.Rect(30, 30, 540, 540)
                if state["game_over"]:
                    continue
                if state["mode"] == "human_ai" and state["current_player"] == config.PLAYER_O:
                    continue
                if not board_rect.collidepoint(event.pos):
                    continue

                cell_size = 540 // config.BOARD_SIZE
                row = (event.pos[1] - board_rect.top) // cell_size
                col = (event.pos[0] - board_rect.left) // cell_size
                if state["mode"] == "human_human":
                    if _apply_move(state, row, col, state["current_player"]):
                        if not state["game_over"]:
                            state["status_text"] = "Đến lượt " + ("X" if state["current_player"] == config.PLAYER_X else "O")
                elif state["mode"] == "human_ai" and state["current_player"] == config.PLAYER_X:
                    if _apply_move(state, row, col, config.PLAYER_X):
                        if not state["game_over"]:
                            state["status_text"] = "Máy đang suy nghĩ..."

        if not state["game_over"]:
            if state["mode"] == "human_ai" and state["current_player"] == config.PLAYER_O:
                search_result = state["ai"].search_alphabeta(2, -math.inf, math.inf, True) if state["ai_mode"] == "alphabeta" else state["ai"].search_minimax(2, True)
                if search_result.move:
                    _apply_move(state, search_result.move[0], search_result.move[1], config.PLAYER_O)
                    if not state["game_over"]:
                        state["status_text"] = f"{search_result.algorithm}: {search_result.move}, score={search_result.score}, nodes={search_result.nodes_explored}, depth={search_result.depth}, time={search_result.elapsed_sec:.4f}s"
            elif state["mode"] == "ai_ai":
                search_result = state["ai"].search_alphabeta(2, -math.inf, math.inf, state["current_player"] == config.PLAYER_O) if state["ai_mode"] == "alphabeta" else state["ai"].search_minimax(2, state["current_player"] == config.PLAYER_O)
                if search_result.move:
                    _apply_move(state, search_result.move[0], search_result.move[1], state["current_player"])
                    if not state["game_over"]:
                        state["status_text"] = f"Máy: {search_result.algorithm} | {search_result.move} | score={search_result.score}"

        board_rect = _draw_grid(screen, state["board"], font, f"Chế độ: {mode_labels[state['mode']]} | {state['status_text']}")
        for button in buttons:
            active = False
            if button.action == "set_mode_human_human" and state["mode"] == "human_human":
                active = True
            if button.action == "set_mode_human_ai" and state["mode"] == "human_ai":
                active = True
            if button.action == "set_mode_ai_ai" and state["mode"] == "ai_ai":
                active = True
            if button.action == "set_ai_minimax" and state.get("ai_mode") == "minimax":
                active = True
            if button.action == "set_ai_alphabeta" and state.get("ai_mode") == "alphabeta":
                active = True
            _draw_button(screen, button_font, button, active=active)

        turn_text = f"Lượt tiếp theo: {'X' if state['current_player'] == config.PLAYER_X else 'O'} | Số nước: {_move_count(state['board'])}"
        turn_label = font.render(turn_text, True, (236, 239, 245))
        screen.blit(turn_label, (30, 755))
        pygame.display.flip()
        clock.tick(30)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Caro AI")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dev", action="store_true", help="Chạy AI vs AI")
    group.add_argument("--benchmark", action="store_true", help="Chạy benchmark")
    parser.add_argument("--depth", type=int, default=2, help="Độ sâu mặc định cho chế độ dev")
    args = parser.parse_args(argv)

    if args.benchmark:
        mode = GameMode.BENCHMARK
    elif args.dev:
        mode = GameMode.DEVELOPER
    else:
        mode = GameMode.NORMAL

    if mode == GameMode.BENCHMARK:
        return benchmark_main()
    if mode == GameMode.DEVELOPER:
        _run_ai_vs_ai(depth=args.depth)
        return 0

    try:
        import pygame  # noqa: F401
    except ModuleNotFoundError:
        _run_human_vs_ai()
        return 0

    _run_pygame_ui()
    return 0
