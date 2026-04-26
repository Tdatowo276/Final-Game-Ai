from src.game_logic import get_valid_moves, simulate_move, minimax


def test_get_valid_moves_returns_only_player_cells():
    board = [10, 5, 0, 2, 0, 1, 10, 3, 0, 4, 0, 0]
    moves_p0 = get_valid_moves(board, 0)
    assert all(index in range(1, 6) for index, _ in moves_p0)
    assert all(board[index] > 0 for index, _ in moves_p0)

    moves_p1 = get_valid_moves(board, 1)
    assert all(index in range(7, 12) for index, _ in moves_p1)
    assert all(board[index] > 0 for index, _ in moves_p1)


def test_simulate_move_captures_correctly():
    # Board chỉ có quân ở vị trí cần test, tránh ăn quân thừa
    board = [10, 1, 0, 0, 3, 0, 10, 0, 0, 0, 0, 0]
    scores = [0, 0]
    new_board, new_scores = simulate_move(board, scores, 1, 1, 0)

    # Rải 1 quân từ ô 1 -> ô 2. Ô 3 trống -> ăn ô 4 (3 quân). Ô 5 trống -> ăn ô 6 (10 quân Quan)
    assert new_scores[0] == 13
    assert new_board[4] == 0
    assert new_board[1] == 0


def test_minimax_returns_move_with_depth():
    board = [10, 0, 0, 0, 3, 0, 10, 1, 0, 0, 0, 0]
    scores = [0, 0]
    value, move_idx, move_dir = minimax(board, scores, 2, float("-inf"), float("inf"), True)

    assert move_idx is not None
    assert move_dir in (-1, 1)
    assert isinstance(value, float)
