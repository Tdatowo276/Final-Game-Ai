import functools
from typing import List, Optional, Tuple


def get_valid_moves(board: List[int], player_idx: int) -> List[Tuple[int, int]]:
    if player_idx == 0:
        indexes = range(1, 6)
    else:
        indexes = range(7, 12)
    return [(i, d) for i in indexes if board[i] > 0 for d in (1, -1)]


def simulate_move(curr_board: List[int], curr_scores: List[int], start_idx: int, direction: int, player_idx: int) -> Tuple[List[int], List[int]]:
    temp_b = curr_board.copy()
    temp_s = curr_scores.copy()
    actual_dir = direction if player_idx == 0 else -direction
    hand = temp_b[start_idx]
    temp_b[start_idx] = 0
    pos = start_idx

    while hand > 0:
        pos = (pos + actual_dir) % 12
        temp_b[pos] += 1
        hand -= 1

    while True:
        next_pos = (pos + actual_dir) % 12
        if temp_b[next_pos] > 0 and next_pos not in (0, 6):
            hand = temp_b[next_pos]
            temp_b[next_pos] = 0
            pos = next_pos
            while hand > 0:
                pos = (pos + actual_dir) % 12
                temp_b[pos] += 1
                hand -= 1
            continue

        if temp_b[next_pos] == 0:
            target = (next_pos + actual_dir) % 12
            if temp_b[target] > 0:
                temp_s[player_idx] += temp_b[target]
                temp_b[target] = 0
            break

        break

    return temp_b, temp_s


def _evaluate_position(board: List[int], scores: List[int]) -> float:
    material_balance = sum(board[7:12]) - sum(board[1:6])
    return (scores[1] - scores[0]) + material_balance * 0.1


@functools.lru_cache(maxsize=None)
def _cached_minimax(board_tuple: tuple[int, ...], scores_tuple: tuple[int, int], depth: int, is_max: bool) -> Tuple[float, Optional[int], Optional[int]]:
    board = list(board_tuple)
    scores = list(scores_tuple)

    if depth == 0 or (board[0] == 0 and board[6] == 0):
        return _evaluate_position(board, scores), None, None

    player_idx = 1 if is_max else 0
    moves = get_valid_moves(board, player_idx)
    if not moves:
        return _evaluate_position(board, scores), None, None

    best_move = (None, None)
    if is_max:
        max_eval = float("-inf")
        for start_idx, direction in moves:
            next_board, next_scores = simulate_move(board, scores, start_idx, direction, player_idx)
            eval_score, _, _ = _cached_minimax(tuple(next_board), tuple(next_scores), depth - 1, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = (start_idx, direction)
        return max_eval, best_move[0], best_move[1]

    min_eval = float("inf")
    for start_idx, direction in moves:
        next_board, next_scores = simulate_move(board, scores, start_idx, direction, player_idx)
        eval_score, _, _ = _cached_minimax(tuple(next_board), tuple(next_scores), depth - 1, True)
        if eval_score < min_eval:
            min_eval = eval_score
            best_move = (start_idx, direction)
    return min_eval, best_move[0], best_move[1]


def minimax(board: List[int], scores: List[int], depth: int, alpha: float, beta: float, is_max: bool) -> Tuple[float, Optional[int], Optional[int]]:
    return _cached_minimax(tuple(board), tuple(scores), depth, is_max)
