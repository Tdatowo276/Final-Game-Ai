import random
from .game_logic import minimax, get_valid_moves


def choose_ai_move(board, score, difficulty):
    valid_moves = get_valid_moves(board, 1)
    if not valid_moves:
        return None, None

    if difficulty == 1 and random.random() < 0.5:#chon che do easy thi xs 50% la đi đại
        return random.choice(valid_moves)
    #else la di theo minimax, do sau phu thuoc vao difficulty
    _, move_idx, move_dir = minimax(board, score, difficulty, float("-inf"), float("inf"), True)
    if move_idx is None:
        return random.choice(valid_moves)
    return move_idx, move_dir
